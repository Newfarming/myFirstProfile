# coding: utf-8

from django.db.models import Q
from django.contrib.auth.models import (
    User
)
from users.models import (
    UserProfile,
)



class AuthPhoneBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):

        user_profile = UserProfile.objects.filter(
                        Q(phone=username) & Q(is_phone_bind=True) | Q(user__username=username)).first()
        if user_profile and user_profile.user.check_password(password):
            return user_profile.user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None