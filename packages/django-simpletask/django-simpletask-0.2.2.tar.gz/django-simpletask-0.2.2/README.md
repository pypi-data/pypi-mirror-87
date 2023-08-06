# django-simpletask

Django application provides simple task model, admin, server services and client service.


## Install

```
pip install django-simpletask
```

## Usage

**pro/settings**

```
INSTALLED_APPS = [
    'django_db_lock',
    'django_simpletask',
]

DJANGO_SIMPLETASK_ACLKEY = "TsE9Jd3TrUtTA9wjGCLXoDqh891srpyo"

```

**Note:**

- Mostly you need a lock service, so we add django_db_lock in INSTALLED_APPS.
- Set DJANGO_SIMPLETASK_ACLKEY to your own aclkey. It will be used in task executor.

**app/models.py**

```
from django_simpletask.models import SimpleTask


class Task(SimpleTask):
    title = models.CharField(max_length=64)

    class Meta:
        permissions = [] + SimpleTask.Meta.permissions

    def do_task_main(self):
        return "done!"

```

**Note:**

- Write your own task model based on SimpleTask.
- Add task reset permission.
- Implement you own do_task_main.

**app/admin.py**

```
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]
    readonly_fields = [] + Task.SIMPLE_TASK_FIELDS
```

**Note:**

- Mostly we don't want to change anything inside task, so we set task fields readonly.

**task_executor.py**

```
from daemon_application.app import DaemonApplication
from django_simpletask.services import SimpleTaskService

class TaskExcutor(DaemonApplication):
    def main(self):
        service = SimpleTaskService("http://127.0.0.1:8000/example/task/services/", aclkey="TsE9Jd3TrUtTA9wjGCLXoDqh891srpyo")
        service.start()
        service.join()

app = TaskExcutor().get_controller()

if __name__ == "__main__":
    app()

```

**Note:**

- Add task_executor.py script.
- Set the server to your own url.
- Set the aclkey match the DJANGO_SIMPLETASK_ACLKEY setting.

## Release

### v0.2.2 2020/12/03

- Long running service don't use database.
- Add aclkey check for simpletask apis.

### v0.1.6 2020/11/17

- Add reset action.
- Add SimpleTask.force_finish.
- Add multi-threads serve.

### v0.1.3 2020/11/09

- Add idle_sleep_time parameter for SimpleTask.serve_forever.

### v0.1.2 2020/11/09

- Add SimpleTask.serve and SimpleTask.serve_forever.

### v0.1.1 2020/10/30

- Add SimpleTask.do_tasks.

### v0.1.0 2020/10/26

- First release.
- Take from django-fastadmin. django-fastadmin should forcus on admin extensions, but NOT abstract models.
