from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.translation import ugettext


def action_reset_task(modeladmin, request, queryset):
    reseted = 0
    for item in queryset.all():
        item.reset(save=True)
        reseted += 1
    modeladmin.message_user(request, ngettext(
        '%d task has been reset.',
        '%d tasks have been reset.',
        reseted,
    ) % reseted, messages.SUCCESS)
action_reset_task.allowed_permissions = ("reset",)
action_reset_task.short_description = ugettext("Reset Selected Tasks: %(verbose_name_plural)s")
