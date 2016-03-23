# coding: utf-8

from django import forms
from django.db import transaction

from resumes.models import (
    ContactInfoData,
    HistoryContactInfo,
)

from Common.forms import (
    NormalizeFormStringMixin,
)

from pin_utils.django_utils import (
    get_object_or_none,
    get_phone,
)


class ContactInfoForm(NormalizeFormStringMixin, forms.ModelForm):

    resume_id = forms.CharField(max_length=100, label=u'ResumeID')
    origin = forms.IntegerField(label=u'来源', initial=1, required=False)

    def clean_origin(self):
        origin = self.data.get('origin')
        if origin not in dict(ContactInfoData.ORIGIN_META).keys():
            return 2
        return origin

    def clean_phone(self):
        clean_phone = self.data.get('phone') or ''
        phone = get_phone(clean_phone)
        if not phone:
            raise forms.ValidationError('电话号码有误')
        return phone

    def get_exist_contact(self):
        resume_id = self.cleaned_data['resume_id']
        contact_info = get_object_or_none(
            ContactInfoData,
            resume_id=resume_id,
        )
        return contact_info

    def has_same_contact(self, exist_contact):
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email']
        exist_phone = get_phone(exist_contact.phone)
        exist_email = exist_contact.email
        return True if phone == exist_phone and email == exist_email else False

    def update_contact_info(self, exist_contact):
        if self.has_same_contact(exist_contact):
            return exist_contact

        source_id = self.cleaned_data['source_id']
        source = self.cleaned_data['source']
        name = self.cleaned_data['name']
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email']
        origin = self.cleaned_data['origin']

        with transaction.atomic():
            HistoryContactInfo.objects.create(
                contact_info=exist_contact,
                resume_id=exist_contact.resume_id,
                source_id=exist_contact.source_id,
                source=exist_contact.source,
                name=exist_contact.name,
                phone=exist_contact.phone,
                email=exist_contact.email,
                qq=exist_contact.qq,
                weibo=exist_contact.weibo,
                identity_id=exist_contact.identity_id,
                reported_num=exist_contact.reported_num,
                status=exist_contact.status or 'public',
                origin=exist_contact.origin,
            )
            exist_contact.source_id = source_id
            exist_contact.source = source
            exist_contact.name = name
            exist_contact.phone = phone
            exist_contact.email = email
            exist_contact.origin = origin
            exist_contact.save()

        return exist_contact

    def create_contact_info(self):
        resume_id = self.cleaned_data['resume_id']
        source_id = self.cleaned_data['source_id']
        source = self.cleaned_data['source']
        name = self.cleaned_data['name']
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email']
        origin = self.cleaned_data['origin']

        contact_info = ContactInfoData.objects.create(
            resume_id=resume_id,
            source_id=source_id,
            source=source,
            name=name,
            phone=phone,
            email=email,
            origin=origin,
            status='public',
        )
        return contact_info

    def save(self):
        exist_contact = self.get_exist_contact()
        if exist_contact:
            contact_info = self.update_contact_info(exist_contact)
        else:
            contact_info = self.create_contact_info()
        return contact_info

    class Meta:
        model = ContactInfoData
        fields = (
            'source_id',
            'source',
            'name',
            'phone',
            'email',
            'origin',
        )
