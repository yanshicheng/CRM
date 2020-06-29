from django import forms
from sales.models import UserProfile, Customer, ConsultRecord, Enrollment, ClassList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# ModelForm
class BootstrapBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给实例对象的每一个字段添加class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-group input-material'})

# ModeForm
class RegForm(BootstrapBaseForm):
    # 重写字段
    # name = forms.CharField(
    #     max_length=16,
    #     min_length=3,
    # )
    # password = forms.CharField(
    #     widget=forms.widgets.PasswordInput(),
    #     max_length=24,
    #     min_length=6,
    # )
    # 自定义字段
    re_password = forms.CharField(
        widget=forms.widgets.PasswordInput(
                attrs={
                    'placeholder': '确认密码',
                }),
        max_length=24,
        min_length=6,
        error_messages= {
                           "required": "密码不能为空",
                           "invalid": "格式错误",
                           "min_length": "密码最小为6位",
                           "max_length": "密码最长为24位",
                       },
    )

    # 类的配置
    class Meta:
        model = UserProfile  # 绑定 orm mode类
        # 展示要显示的字段
        fields = ['name', 'email', 'password', 're_password', 'mobile']
        # exclude = []  # 吧不需要展示的字段排除
        # 错误提示
        error_messages = {
            'name': {
                "required": "用户名不能为空",
                "invalid": "格式错误",
                "min_length": "用户名最小为3位",
                "max_length": "用户名最长为16位",
            },
            'mobile': {
                "required": "手机号不能为空",
                "invalid": "请输入正确手机号",
                "min_length": "请输入正确手机号",
                "max_length": "请输入正确手机号",
            },
            'password': {
                "required": "密码不能为空",
                "invalid": "格式错误",
                "min_length": "密码最小为6位",
                "max_length": "密码最长为24位",
            },

            'email': {
                "required": "邮箱不能为空",
                "invalid": "请输入正确邮箱地址",
                "min_length": "请输入正确邮箱地址",
                "max_length": "请输入正确邮箱地址",
            },
        }

        # labels 标签
        labels = {

        }

        # 插件
        widgets = {
            'name': forms.widgets.TextInput(
                attrs={
                    'placeholder': '用户名',
                }),

            'email': forms.widgets.EmailInput(
                attrs={
                    'placeholder': '邮  箱',
                }
            ),
            'mobile': forms.widgets.TextInput(
                attrs={
                    'placeholder': '手机号',
                }
            ),
            'password': forms.widgets.PasswordInput(
                attrs={
                    'placeholder': '密  码',
                }
            ),

        }

    # # 初始化
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs.update({'class': 'form-group input-material'})



    # 检查邮箱是否被注册
    def clean_email(self):
        email_value = self.cleaned_data.get('email')
        is_exist = UserProfile.objects.filter(email=email_value)
        if is_exist:
            raise ValidationError('邮箱已被注册')
        else:
            return email_value
    # 检查手机号是否被注册
    def clean_mobile(self):
        mobile_value = self.cleaned_data.get('mobile')
        is_exist = UserProfile.objects.filter(mobile=mobile_value)
        if is_exist:
            raise ValidationError('手机号已被注册')
        else:
            return mobile_value

    # 检查两次密码输入是否一致
    def clean(self):
        pwd_value = self.cleaned_data.get('password')
        re_pwd_value = self.cleaned_data.get('re_password')
        if pwd_value == re_pwd_value:
            return self.cleaned_data
        else:
            self.add_error('re_password', '两次密码不一致')
            raise ValidationError('两次密码不一致')

# 编辑 FoRM
class CustomerForm(BootstrapBaseForm):
    # def __init__(self,*args,**kwargs):
    #     super(CustomerForm,self).__init__(*args,**kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple,
            'birthday': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

# 沟通记录的form
class ConsultRecordForm(BootstrapBaseForm):
    class Meta:
        model = ConsultRecord
        exclude = ['delete_status', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 把customer字段的choice设置成我的客户
        print(self.instance, id(self.instance))
        print('&' * 120)
        # 方法1：修改字段的chocies选项
        # self.fields['customer'].choices = Customer.objects.filter(consultant=self.instance.consultant).values_list('id','name')
        # 方法2：将form表的字段直接修改字段
        self.fields['customer'] = forms.models.ModelChoiceField(queryset=Customer.objects.filter(consultant=self.instance.consultant))
        self.fields['customer'].widget.attrs.update({'class': 'form-control'})
        # 修改跟进人只能是自己
        self.fields['consultant'].choices = [(self.instance.consultant.id, self.instance.consultant.name), ]


# 报名表
class EnrollmentForm(BootstrapBaseForm):

    class Meta:
        model = Enrollment
        exclude = ['contract_approved', 'delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制添加报名表的时候只能选自己私户
        # print(self.instance)
        self.fields['customer'].choices = [(self.instance.customer.id, self.instance.customer.name)]



# 班级表
class ClassListForm(BootstrapBaseForm):

    class Meta:
        model = ClassList
        fields = '__all__'
