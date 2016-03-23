# coding: utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from django.contrib.auth.models import User

from transaction.models import UserChargePackage
from app.payment.models import PaymentOrder


def pkg2payment_order():
    user_pkgs = UserChargePackage.objects.select_related(
        'package',
        'feed_service',
    ).filter(
        order=None,
    )

    for pkg in user_pkgs:
        if pkg.resume_package and (not pkg.resume_package.display and pkg.actual_cost <= 0):
            continue

        if pkg.feed_package and (not pkg.feed_package.display and pkg.actual_cost <= 0):
            continue

        try:
            user = pkg.user
        except User.DoesNotExist:
            continue

        if pkg.resume_package:
            order = PaymentOrder(
                user=user,
                package=pkg.resume_package,
                package_price=pkg.actual_cost,
            )
        else:
            order = PaymentOrder(
                user=user,
                feed_service=pkg.feed_package,
                feed_price=pkg.actual_cost,
                feed_count=pkg.extra_feed_num,
            )

        order.add_order_id()
        order.pay_status = 'paid' if pkg.pay_status == 'finished' else 'unpay'
        order.total_price = pkg.actual_cost
        order.actual_price = pkg.actual_cost
        order.payment_terms = 'offline'
        order.save()

        order.create_time = pkg.start_time
        order.save()

        pkg.order = order
        pkg.save()


def delete_useless_order():
    PaymentOrder.objects.filter(
        userchargepackage=None,
    ).delete()


if __name__ == '__main__':
    pkg2payment_order()
    # delete_useless_order()
