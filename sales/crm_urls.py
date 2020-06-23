"""
crm app路由匹配规则
所有以crm开头的请求都会转到这里来做后续的匹配
"""

from django.conf.urls import url
from sales import views


urlpatterns = [
    # url(r'customer_list/$', views.customer_list),
    url(r'customer_list/$', views.customer_list, name='customer_list'),
    url(r'add_customer/$', views.add_customer, name='add_customer'),
    url(r'edit_customer/(\d+)/$', views.edit_customer, name='edit_customer'),
]