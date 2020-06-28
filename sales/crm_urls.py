"""
crm app路由匹配规则
所有以crm开头的请求都会转到这里来做后续的匹配
"""

from django.conf.urls import url
from sales import views


urlpatterns = [
    # url(r'customer_list/$', views.customer_list),
    url(r'customer_list/$', views.CustomerListVuew.as_view(), name='customer_list'), # 全部的客户信息
    url(r'my_customer/$', views.CustomerListVuew.as_view(), name='my_customer'), # 我的客户信息
    # url(r'add_customer/$', views.add_customer, name='add_customer'),
    # url(r'edit_customer/(\d+)/$', views.edit_customer, name='edit_customer'),
    url(r'add_customer/$', views.customer, name='add_customer'),
    url(r'edit_customer/(\d+)/$', views.customer, name='edit_customer'),
]