from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from api_basebone.core.fields import BoneImageUrlField
from lightning.fields import ImageURLField
from werkzeug import Local


class Image(models.Model):
    url = ImageURLField('链接')
    name = models.CharField('文件名', max_length=200, null=True, blank=True)
    create_time = models.DateTimeField('上传时间', auto_now_add=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name='上传者')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'
    
    class GMeta:
        title_field = 'name'
        creator_field = 'create_by'


class AbstractCustomer(models.Model):
    name = models.CharField('名字', max_length=100)
    description = models.CharField('简介', max_length=1024, null=True, blank=True)
    avatar = ImageURLField('头像', blank=True, null=True)
    is_organization = models.BooleanField('是否机构', default=False)
    org_name = models.CharField('机构全称', max_length=200, null=True, blank=True)
    org_code = models.CharField('机构代码', max_length=200, null=True, blank=True)
    phone = models.CharField('电话', max_length=20, null=True, blank=True)
    address = models.CharField('地址', max_length=300, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, null=True, blank=True)
    weixin = models.CharField('微信号', max_length=100, null=True, blank=True)
    qq = models.CharField('QQ号', max_length=100, null=True, blank=True)
    identity_code = models.CharField('身份证号', max_length=100, null=True, blank=True)
    stage = models.CharField('阶段', max_length=20, choices=settings.LIGHTNING_CRM_CUSTOMER_STAGES, default='')
    source = models.CharField('渠道来源', max_length=100, choices=settings.LIGHTNING_CRM_CUSTOMER_SOURCE, default='')
    referrer = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, verbose_name='引荐客户')
    follwer = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name='跟进人', related_name='following_customers')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, verbose_name='创建人', related_name='created_customers')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = '客户'
        verbose_name_plural = '客户'

    class GMeta:
        title_field = 'name'
        creator_field = 'create_by'


class Customer(AbstractCustomer):

    class Meta(AbstractCustomer.Meta):
        swappable = 'LIGHTNING_CRM_CUSTOMER_MODEL'


class Contact(models.Model):
    customer = models.ForeignKey(settings.LIGHTNING_CRM_CUSTOMER_MODEL, models.SET_NULL, 
        null=True, blank=True, verbose_name='客户')
    description = models.CharField('简介', max_length=1024, null=True, blank=True)
    name = models.CharField('名字', max_length=100)
    title = models.CharField('职位', max_length=100, null=True, blank=True)
    avatar = ImageURLField('头像', blank=True, null=True)
    phone = models.CharField('电话', max_length=20, null=True, blank=True)
    address = models.CharField('地址', max_length=300, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, null=True, blank=True)
    weixin = models.CharField('微信号', max_length=100, null=True, blank=True)
    qq = models.CharField('QQ号', max_length=100, null=True, blank=True)
    identity_code = models.CharField('身份证号', max_length=100, null=True, blank=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True,
        blank=True, verbose_name='创建人')

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = '联系人'
    
    class GMeta:
        title_field = 'name'
        creator_field = 'create_by'


class FollowUp(models.Model):
    customer = models.ForeignKey(settings.LIGHTNING_CRM_CUSTOMER_MODEL, models.SET_NULL,
        null=True, blank=True, verbose_name='客户')
    action_type = models.CharField('跟进类型', max_length=50, 
        choices=settings.LIGHTNING_CRM_FOLLOWUP_TYPE,default='')
    content = models.TextField('跟进内容', null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True, verbose_name='图片')
    contacts = models.ManyToManyField(Contact, blank=True, verbose_name='联系人')
    follow_up_time = models.DateTimeField('创建时间', auto_now_add=True)
    follow_up_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
        null=True, blank=True, verbose_name='跟进人')

    class Meta:
        verbose_name = '跟进'
        verbose_name_plural = '跟进'

    class GMeta:
        creator_field = 'follow_up_by'