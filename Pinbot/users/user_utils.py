# coding: utf-8


class UserUtils(object):

    @classmethod
    def update_guide_switch(cls, user, guide_switch=False):
        user.userprofile.guide_switch = guide_switch
        user.userprofile.save()
        return user
