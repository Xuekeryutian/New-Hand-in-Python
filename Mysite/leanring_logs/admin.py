from django.contrib import admin
from leanring_logs.models import Topic,Entry
# Register your models here.

admin.site.register(Topic)
admin.site.register(Entry)