import logging
import json
import time
from urllib import parse as urlparse

import requests
from fastutils import sysutils
from fastutils import threadutils
from fastutils import threadutils


logger = logging.getLogger(__name__)


class SimpleTaskService(threadutils.SimpleProducerConsumerServerBase):
    default_produce_loop_interval = 1
    default_queue_size = 10

    def __init__(self, server, aclkey, task_id_field_name="pk", batch_size=5, api_url_get_ready_tasks=None, api_url_do_task=None, **kwargs):
        self.server = server
        self.aclkey = aclkey
        self.batch_size = batch_size
        self.task_id_field_name = task_id_field_name
        self.executorName = sysutils.get_worker_id("SimpleTaskService")
        self.api_url_get_ready_tasks = api_url_get_ready_tasks or urlparse.urljoin(self.server, "./getReadyTasks")
        self.api_url_do_task = api_url_do_task or urlparse.urljoin(self.server, "./doTask")
        super().__init__(**kwargs)

    def produce(self):
        params = {
            "aclkey": self.aclkey,
            "executorName": self.executorName,
            "batchSize": self.batch_size,
            "ts": time.time(),
        }
        logger.info("calling get_ready_tasks api: url={}, params={}".format(self.api_url_get_ready_tasks, params))
        response = requests.get(self.api_url_get_ready_tasks, params)
        logger.info("calling get_ready_tasks api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        tasks = response_package["result"]
        return tasks

    def consume(self, task):
        params = {
            "taskId": task[self.task_id_field_name],
            "aclkey": self.aclkey,
            "executorName": self.executorName,
            "ts": time.time(),
        }
        logger.info("calling do_task api: url={}, params={}".format(self.api_url_do_task, params))
        response = requests.get(self.api_url_do_task, params)
        logger.info("calling get_ready_tasks api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        tasks = response_package["result"]
        return tasks

    @classmethod
    def serve(cls, **kwargs):
        service = cls(**kwargs)
        service.start()
        return service

