from django.contrib import admin

# Register your models here.

from .models import Attendance
from .models import Leave
from .models import Rebate

admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Rebate)


