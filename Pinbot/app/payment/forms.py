# coding: utf-8

import datetime

from django import forms

from pinbot_package.models import (
    ResumePackge,
    FeedService,
)
from transaction.models import (
    UserChargePackage
)
from models import (
    ShoppingCar,
    BillInfo,
    ReceiverInfo,
)

from pin_utils.django_utils import (
    get_object_or_none,
    get_int,
    error_phone,
)
from pin_utils.form_mixin import (
    FormErrors,
)


class ShoppingCarForm(forms.ModelForm, FormErrors):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ShoppingCarForm, self).__init__(*args, **kwargs)

    def clean_package(self):
        package_id = self.data.get('package')

        if not package_id:
            user = self.request.user
            now = datetime.datetime.now()
            order = UserChargePackage.objects.filter(
                user=user,
                resume_end_time__gt=now,
                pay_status='finished',
            )
            if not order:
                raise forms.ValidationError(u'请选择简历套餐')
            return None

        display_package = get_object_or_none(
            ResumePackge,
            display=1,
            id=package_id,
        )
        if not display_package:
            raise forms.ValidationError(u'简历套餐无效，请选择有效的套餐')
        return display_package

    def clean_feed_service(self):
        feed_service_id = self.data['feed_service']

        if not feed_service_id:
            return None

        feed_service = get_object_or_none(
            FeedService,
            display=1,
            id=feed_service_id,
        )
        if not feed_service:
            raise forms.ValidationError(u'定制服务无效，请选择有效的定制')
        return feed_service

    def clean_feed_count(self):
        feed_service = self.data['feed_service']
        if not feed_service:
            return 0

        feed_count = get_int(self.data['feed_count'])
        if feed_count < 1:
            raise forms.ValidationError(u'订阅数至少需要一个')
        return feed_count

    class Meta:
        model = ShoppingCar
        exclude = ['user', 'package_price', 'feed_price', 'total_price']


class BillInfoForm(forms.ModelForm, FormErrors):

    def clean_title(self):
        bill_type = self.data['bill_type']
        title = self.data['title']

        if bill_type == 'company' and not title:
            raise forms.ValidationError(u'发表抬头必填')
        return title

    class Meta:
        model = BillInfo
        exclude = ['user']


class ReceiverInfoForm(forms.ModelForm, FormErrors):

    def clean_phone(self):
        phone = self.data['phone']

        if error_phone(phone):
            raise forms.ValidationError(
                u'电话号码格式错误，请填写正确的手机号或者座机号，<br />如：18042412009，07735422199，40000001111'
            )
        return phone

    class Meta:
        model = ReceiverInfo
        exclude = ['user', 'default_addr']
