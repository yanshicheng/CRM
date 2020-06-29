"""
crm app路由匹配规则
所有以crm开头的请求都会转到这里来做后续的匹配
"""

from django.conf.urls import url
from sales import views,ajax_views


urlpatterns = [
    # url(r'customer_list/$', views.customer_list),
    url(r'customer_list/$', views.CustomerListVuew.as_view(), name='customer_list'), # 全部的客户信息
    url(r'my_customer/$', views.CustomerListVuew.as_view(), name='my_customer'), # 我的客户信息
    # url(r'add_customer/$', views.add_customer, name='add_customer'),
    # url(r'edit_customer/(\d+)/$', views.edit_customer, name='edit_customer'),
    url(r'add_customer/$', views.customer, name='add_customer'),        #
    url(r'edit_customer/(\d+)/$', views.customer, name='edit_customer'),

    ########### 沟通记录 ##########
    url(r'^consult_record/(?P<cid>\d+)/$',views.consult_record_list,name='consult_record'),
    url(r'^add_consult_record/$', views.consult_record, name='add_record'),  # 添加沟通记录
    url(r'^edit_consult_record/(\d+)$', views.consult_record, name='edit_record'),  # 编辑沟通记录

    ######### 报名记录相关 ########
    # 报名表
    url(r'^enrollment_list/(?P<customer_id>\d+)/$', views.EnrollmentListView.as_view(), name='enrollment_list'),
    # 查看报名记录
    url(r'^add_enrollment/(?P<customer_id>\d+)/$', views.enrollment, name='add_enrollment'),
    url(r'^edit_enrollment/(?P<enrollment_id>\d+)/$', views.enrollment, name='edit_enrollment'),

    # AJAX
    url(r'^ajax_class/$', ajax_views.ajax_class),

]