from django.shortcuts import render,HttpResponse,redirect
from django import views
from sales.models import UserProfile,Customer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from sales.forms import RegForm,CustomerForm
from django.contrib import auth
from django.urls import reverse

# 导入分页类
from utils.mypage import Pagination

class login(views.View):
    def get(self,request):
        rep = render(request, 'login.html')
        return rep
    def post(self,request):
        print(request.POST)
        email = request.POST.get('Email')
        pwd = request.POST.get('passWord')
        # 获取用户是否勾选七天免登录
        remember_7 = request.POST.get('check1',None)
        user_obj = auth.authenticate(request,email=email,password=pwd)
        if user_obj:
            # 获取用户上个页面跳转的 地址 如果没有获取到则设置 默认值
            return_url = request.GET.get('return_Url','/home/')
            print(return_url)
            # 设置 session 字典属性
            auth.login(request, user_obj)
            # 进行判断
            if remember_7:
                # 如果用户勾选七天免登录则设置 session 过期时间
                request.session.set_expiry(7*24*60*60)
            else:
                # 如果用户没有勾选则设置 session 过期时间为0
                request.session.set_expiry(0)

            return redirect(return_url)
        return render(request, 'login.html',{'msg':'用户名或密码错误!'})





class register(views.View):
    def get(self,request):
        form_obj = RegForm()
        return render(request,'register.html', {'form':form_obj},)
    def post(self,request):
        res = {'code':0}
        # 利用 post 提交的数据实例化 form 类
        form_obj = RegForm(request.POST)
        print(form_obj)
        # 校验数据的有效性
        if form_obj.is_valid():
            # 方法1
            # 1.1  移除 re_password
            # form_obj.cleaned_data.pop('re_password')
            # 2.2
           # UserProfile.objects.create(**form_obj.cleaned_data)
            # 方法2
            user_obj = form_obj.save()  # from_obj 是一个 MofelFrom 对象,他和数据里面的Model类相对应
            user_obj.set_password(user_obj.password)
            user_obj.save()
            res['url'] = '/login/'
        else:
            # 数据有问题
            res['code'] = 1
            res['error_msg'] = form_obj.errors
        return JsonResponse(res)


@login_required
def homeVie(request):
    return render(request,'home.html')


# 查看用户表
def customer_list(request):
    index_page = request.GET.get('page', 1)
    url_prefix = request.path_info

    # 获取所有客户信息进行展示
    query_set = Customer.objects.all()
    all_data = query_set.count()
    print(all_data)
    page_obj = Pagination(index_page,all_data,url_prefix='/crm/customer_list/')
    # current_page = request.GET.get('page',1)
    # page_obj = Pagination(current_page,query_set.count(),url_prefix,per_page=2)
    # data = query_set[page_obj.start:page_obj.end] 'page_html':html_page
    data = query_set[page_obj.start:page_obj.end]
    page_html = page_obj.page_html
    # 在页面上展示出来
    return render(request,'customer_list.html',{'customer_list':data,'page_html':page_html})




####### 版本一

def add_customer(request):
    form_obj = CustomerForm()
    if request.method == 'POST':
        customer_obj = None
        form_obj = CustomerForm(request.POST, instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request,'add_customer.html',{'form_obj':form_obj})

def edit_customer(request,edit_id):
    customer_obj = Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=customer_obj)

    # 使用instance对象的数据填充生成input标签
    form_obj = CustomerForm(instance=customer_obj)
    if request.method == 'POST':
        # 使用POST提交的数据去更新指定的instance实例
        form_obj = CustomerForm(request.POST, instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))

    return render(request, 'edit_customer.html', {'form_obj': form_obj})


# 注销函数
def logout(request):
    auth.logout(request)
    return redirect('/login/')
