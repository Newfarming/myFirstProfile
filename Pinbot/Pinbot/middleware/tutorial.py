# coding: utf-8

from django.shortcuts import redirect

from app.vip.vip_utils import VipRoleUtils


class TutorialMiddleware(object):

    redirect_url = '/tut/'
    include_url_prefix = (
        '/resumes',
        '/feed',
        '/transaction',
        '/jobs',
        '/promotion_point',
        '/special_feed',
        '/companycard',
        '/payment',
        '/tut',
    )

    def process_request(self, request):
        user = request.user
        if not user.is_authenticated():
            return None

        if hasattr(user, 'userprofile') and not user.userprofile.guide_switch:
            return None

        current_url_path = request.path
        is_include_url = filter(
            lambda x: current_url_path.startswith(x),
            self.include_url_prefix
        )

        if is_include_url:
            user.userprofile.guide_switch = False
            user.userprofile.save()
            return redirect(self.redirect_url)
        return None
