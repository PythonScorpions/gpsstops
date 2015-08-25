'''
'''
from django.db.models import Q


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