'''
'''
from django.db.models import Q

from accounts.models import *


def filter_objects_by_user(user, model_class):
    if user.user_profiles.user_role == "super_admin":
        objects = model_class.objects \
                    .filter(
                        Q(user=user) |
                        Q(user__user_profiles__admin=user) |
                        Q(user__user_profiles__admin__user_profiles__admin=user)
                    )
    elif user.user_profiles.user_role == "admin":
        objects = model_class.objects \
                    .filter(
                        Q(user=user) |
                        Q(user__user_profiles__admin=user) |
                        Q(user__user_profiles__admin=user.user_profiles.admin)
                    )
    else:
        objects = model_class.objects.filter(user=user)
    return objects


def get_users(user):
    if user.user_profiles.user_role == "super_admin":
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin__user_profiles__admin=user)
                ) \
                .exclude(pk=user.id)
    else:
        users = User.objects \
                .filter(
                    Q(user_profiles__admin=user) |
                    Q(user_profiles__admin=user.user_profiles.admin)
                ) \
                .filter(user_profiles__user_role="employee") \
                .exclude(pk=user.id)

    return users
