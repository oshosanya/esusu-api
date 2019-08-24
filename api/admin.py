# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import SavingsGroup, SavingsGroupMember

# Register your models here.
admin.site.register(SavingsGroup)
admin.site.register(SavingsGroupMember)
