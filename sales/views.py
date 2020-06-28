from django.shortcuts import render,HttpResponse,redirect
from django import views
from sales.models import UserProfile,Customer
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from sales.forms import RegForm,CustomerForm
from django.contrib import auth
from django.urls import reverse
from copy import deepcopy
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import QueryDict


# 导入分页类发
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
class CustomerListVuew(views.View):
    @method_decorator(login_required)
    def get(self,request):
        url_prefix = request.path_info

        # 模糊搜索的参数传入 Pagination 分页方法中
        qd = deepcopy(request.GET)  # <QueryDict: {'query': ['了']}>
        qd._mutable = True  # 让QueryDict对象可修改

        current_page = request.GET.get('page', 1)
        if request.path_info == reverse('my_customer'):
            # 获取所有客户信息进行展示
            query_set = Customer.objects.filter(consultant=request.user) # 获取当前 登录的人
        else:
            # 获取所有公户信息
            query_set = Customer.objects.filter(consultant__isnull=True)    # 基于双下划綫找到 cinsultant 字段为空的数据
        # 根据模糊检索的条件对 query_set 做过滤
        # 找到 name,qq,qq_name,字段包含 query_value的那些数据,这些数据就是模糊搜索的结果
        q = self._fuzzy_search(['name','qq','qq_name'])
        query_set = query_set.filter(q)

        # 取到所有数据的总和
        all_data = query_set.count()
        print(all_data)
        page_obj = Pagination(current_page,all_data,url_prefix,qd,per_page=5)

        # 切片取到展示的数据
        data = query_set[page_obj.start:page_obj.end]
        # 返回页码
        page_html = page_obj.page_html
        # 在页面上展示出来
        return render(request,'customer_list.html',{'customer_list':data,'page_html':page_html})
    @method_decorator(login_required)
    def post(self,request):
        # 批量操作 (变公户/变私户)
        cid  = request.POST.getlist('cid')  # 获取要操作的客户的 id
        action = request.POST.get('action') # 获取要执行的方法
        # 判断 self 是否有一个 _action 的方法,如果有就执行,否则就返回 404
        if not hasattr(self,f'_{action}'):
            return HttpResponse('404')
        getattr(self,f'_{action}')(cid)
        return redirect(reverse('customer_list'))

    # 定义批量变为私户的函数
    def _to_private(self,cid):
        # 方法1: 找到要操作的客户数据,把他们变为我的客户
        # Customer.objects.filter(id__in=cid).update(consultant=register.user)
        # 方法2: 把要操作的客户添加到我的客户列表中
        self.request.user.customers.add(*Customer.objects.filter(id__in=cid))

    # 定义批量变为公户的函数
    def _to_public(self,cid):
        # 方法1: 找到要操作的客户的数据,把他们的销售字段置为空
        Customer.objects.filter(id__in=cid).update(consultant=None)
        # 方法2: 从我的客户列表里面吧指定的客户删掉
        # self.request.user.customers.remove(*Customer.objects.filter(id__in=cid))

    # 定义一个模糊检索的方法
    def _fuzzy_search(self,field_list,op='OR'):
        # 从 URL 中取到 query 参数
        query_value = self.request.GET.get('query','')
        q = Q()
        q.connector = op
        for field in field_list:
            q.children.append(Q((f'{field}__icontains', query_value)))
        return q

####### 版本一 ================
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

############## 编辑客户 版本 二 ===============
def customer(request,edit_id=None):
    # 如果edit_id=None表示是新增操作
    # 如果edit_id有值表示是编辑操作
    # ret = Customer.objects.filter(pk=10000000).first()
    # print(ret)
    customer_obj = Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=customer_obj)
    if request.method == "POST":
        # 使用 POST 提交的数据去更新指定的 instance 实例
        form_obj = CustomerForm(request.POST,instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            # 如果能从 URL 获取到 next 参数就跳转到指定的 URL, 没有就默认跳转到客户列表页面.
            next_url = request.GET.get('next',reverse('customer_list'))
            return redirect(next_url)
    return render(request,'customer.html',{'form_obj': form_obj, 'edit_id': edit_id})

# 注销函数
def logout(request):
    auth.logout(request)
    return redirect('/login/')
