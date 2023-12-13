from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().select_related('industrial_worker').select_related('industrial_worker__company')
