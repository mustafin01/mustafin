from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Application)
admin.site.register(Status)