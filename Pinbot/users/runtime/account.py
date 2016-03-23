# coding: utf-8

from django.contrib.auth.models import (
    User
)
from pin_utils.django_utils import (
    get_object_or_none
)
from users.models import (
    UserProfile
)
from app.vip.runtime.self_service import(
    SelfService
)
from app.vip.vip_utils import VipRoleUtils


class PinbotAccount(object):

    @classmethod
    def get_profile(self, **kwargs):
        return get_object_or_none(UserProfile, **kwargs)

    @classmethod
    def update_user_mobile(self, user, mobile):
        user_obj = user.userprofile if hasattr(user, 'userprofile') else None
        if not user_obj:
            return False

        user_obj.phone = mobile
        user_obj.is_phone_bind = True
        user_obj.save()
        return True

    @classmethod
    def update_user_notify_email(self, user, email):
        user_obj = get_object_or_none(UserProfile, user=user)
        user_obj.user_email = email
        user_obj.is_email_bind = True
        user_obj.save()
        return True

    @classmethod
    def change_user_pwd(self, user_id, password):

        user_obj = get_object_or_none(User, id=user_id)
        user_obj.set_password(password)
        user_obj.save()
        return True

    @classmethod
    def is_phone_bind(self, mobile):
        return get_object_or_none(UserProfile, phone=mobile, is_phone_bind=True)

    @classmethod
    def is_email_bind(self, email):
        return get_object_or_none(UserProfile, user_email=email, is_email_bind=True)

    def active_experience_service(self, user):
        experience_service = VipRoleUtils.get_experience_vip()
        srv_meta = {
            'service_name': 'self_service',
            'product': experience_service,
            'user': user,
        }
        experience_srv = SelfService(**srv_meta)
        srv = experience_srv.create_service()
        ret = experience_srv.active_service() if srv else False
        return ret