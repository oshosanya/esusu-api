# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.
class SavingsGroup(models.Model):
    name = models.TextField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.name)


class SavingsGroupMember(models.Model):
    savings_group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_saved = models.FloatField(null=True)

    def __str__(self):
        return str(self.user.username + ' - ' + self.savings_group.name)


class SavingsGroupInvite(models.Model):
    savings_group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.invitee.username + ' invited to ' + self.savings_group.name + 'by' + self.savings_group.owner.username)

    class Meta:
        unique_together = ['savings_group', 'invitee']
