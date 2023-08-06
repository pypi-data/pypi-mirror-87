import time
import datetime
import logging

import bizerror
from fastutils import sysutils
from fastutils import funcutils

from django.db import models
from django.db import close_old_connections
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

from . import services

logger = logging.getLogger(__name__)

class SimpleTask(models.Model):
    """
    """
    NEW = 0
    READY = 10
    DOING = 20
    DONE = 30
    FAILED = 40

    GET_READY_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:getReadyTasks:Lock"
    GET_READY_TASKS_LOCK_TIMEOUT = 60

    RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:resetDeadTasks:Lock"
    RESET_DEAD_TASKS_LOCK_TIMEOUT = 60
    TASK_DOING_TIMEOUT = 60*5

    STATUS_CHOICES = [
        (NEW, _("Task New")),
        (READY, _("Task Ready")),
        (DOING, _("Task Doing")),
        (DONE, _("Task Done")),
        (FAILED, _("Task Failed")),
    ]


    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW, null=True, blank=True, verbose_name=_("Status"), help_text=_("Task has New, Ready, Doing, Done and Failed status."))
    active = models.NullBooleanField(verbose_name=_("Active"), help_text=_("The task is to be runned or is running..."))
    worker = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Worker ID"))

    success = models.NullBooleanField(verbose_name=_("Success"), help_text=_("Task success or not."))
    result = models.TextField(null=True, blank=True, verbose_name=_("Result"))
    error_code = models.IntegerField(null=True, blank=True, verbose_name=_("Error Code"))
    error_message = models.TextField(null=True, blank=True, verbose_name=_("Error Message"))

    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"), help_text=_("Task add time is the time when the task created."))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"), help_text=_("Task modify time is the time when the task modified."))
    ready_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Ready Time"), help_text=_("Task ready time is the time when the task set ready. Task can only start after READY."))
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Start Time"), help_text=_("Task start time is the time when the task start to run."))
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Expire Time"), help_text=_("Task expire time is the time when the task deactived. A task is expired, it will never be runned, even it is not runned yet."))
    done_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Done Time"), help_text=_("Task done time is the time when the task finished ."))

    auto_ready = True

    class Meta:
        abstract = True
        permissions = [
            ("reset", _("Can reset %(verbose_name_plural)s")),
        ]

    SIMPLE_TASK_FIELDS = [
        "status",
        "active",
        "worker",

        "success",
        "result",
        "error_code",
        "error_message",

        "add_time",
        "ready_time",
        "start_time",
        "expire_time",
        "done_time",
        "mod_time",
    ]

    def get_active_status(self):
        if self.status in [self.DONE, self.FAILED]:
            return False
        if self.expire_time and self.expire_time < timezone.now():
            return False
        return True

    def save(self, *args, **kwargs):
        if (not self.pk) and (not self.status):
            self.reset()
        self.active = self.get_active_status()
        super().save(*args, **kwargs)

    def do_task(self, worker):
        logger.debug("calling do_task, task={}, worker={}".format(self, worker))
        if worker != self.worker:
            raise RuntimeError("Tasks locked by another executor: {} but you are {}.".format(self.worker, worker))
        try:
            logger.debug("calling do_task_main, task={}, worker={}".format(self, worker))
            result = self.do_task_main()
            logger.debug("calling do_task_main, task={}, worker={} result={}".format(self, worker, result))
            self.report_success(worker, result, save=True)
            return True
        except Exception as error:
            logger.exception("calling do_task_main failed.")
            error = bizerror.BizError(error)
            self.report_error(worker, error.code, error.message, save=True)
            raise error

    def do_task_main(self):
        raise NotImplementedError()

    def force_finish(self, success=True, result=True, error_code=None, error_message=None, save=True):
        self.worker = "Application Force Finish"
        self.status = self.DONE
        self.active = False
        self.done_time = timezone.now()
        self.success = success
        self.result = result
        self.error_code = error_code
        self.error_message = error_message
        if save:
            self.save()

    def reset(self, ready_time=None, ready_timeout=None, expire_time=None, save=False):
        self.status = self.NEW
        self.active = False
        self.worker = None
        self.ready_time = None
        self.start_time = None
        self.expire_time = None
        self.done_time = None
        self.success = None
        self.result = None
        self.error_code = None
        self.error_message = None
        if self.auto_ready:
            self.ready(ready_time=ready_time, ready_timeout=ready_timeout, expire_time=expire_time, save=False)
        if save:
            self.save()

    def ready(self, ready_time=None, ready_timeout=None, expire_time=None, save=False):
        if self.status != self.NEW:
            return False
        self.status = self.READY
        self.active = True
        self.ready_time = ready_time or timezone.now()
        if expire_time:
            self.expire_time = expire_time
        elif ready_timeout:
            self.expire_time = self.ready_time + datetime.timedelta(seconds=ready_timeout)
        if save:
            self.save()
        return True

    def start(self, worker, save=False):
        if self.status != self.READY:
            return False
        self.status = self.DOING
        self.worker = worker
        self.start_time = timezone.now()
        if save:
            self.save()
        return True

    def report_success(self, worker, result, save=False):
        if self.worker != worker:
            return False
        if self.status != self.DOING:
            return False
        self.status = self.DONE
        self.active = False
        self.success = True
        self.result = result
        self.done_time = timezone.now()
        if save:
            self.save()
        return True

    def report_error(self, worker, error_code, error_message, save=False):
        if self.worker != worker:
            return False
        if self.status != self.DOING:
            return False
        self.status = self.FAILED
        self.active = False
        self.success = False
        self.error_code = error_code
        self.error_message = error_message
        self.done_time = timezone.now()
        if save:
            self.save()
        return True

    @classmethod
    @funcutils.try_again_on_error(callback=close_old_connections)
    def do_tasks(cls, lock_service=None, woker=None, batch_size=None, loop_sleep=None):
        lock_service = lock_service or cls.get_default_lock_service()
        worker_id_prefix = settings.WSGI_APPLICATION.split(".")[0]
        worker = woker or sysutils.get_worker_id(prefix=worker_id_prefix)
        service = services.SimpleTaskService(cls, lock_service)
        batch_size = batch_size or getattr(cls, "do_tasks_batch_size", 10)
        loop_sleep = loop_sleep or getattr(cls, "do_tasks_loop_sleep", 2)
        while True:
            result = service.do_tasks(worker, n=batch_size)
            logger.info("do tasks result: {0}".format(str(result)))
            time.sleep(loop_sleep)

    @classmethod
    def get_default_lock_service(cls):
        from django_db_lock.client import get_default_lock_service
        return get_default_lock_service()
