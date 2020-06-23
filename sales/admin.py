from django.contrib import admin

# Register your models here.
from sales.models import Customer, ClassList, Campuses
# Register your models here.


# 注册我们自己写的model类
admin.site.register(Customer)
admin.site.register(ClassList)
admin.site.register(Campuses)
