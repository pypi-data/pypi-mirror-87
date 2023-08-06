from datetime import datetime
from django.db import models

from .commands_manager_command import Command


class Group(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        db_table = 'commands_manager_group'
        indexes = [
            models.Index(fields=["name"],),
        ]

    def call_commands(self):
        command_list = list(Command.objects.filter(
            group=self).exclude(is_disabled=True).all())
        for command in command_list:
            if command.is_pending or not command.completed_at or datetime.now() >= command.expired_at:
                command.call_command()
