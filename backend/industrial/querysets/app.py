from django.db import models


class CustomAppManager(models.Manager):

    def get_selected_all_info_selected(self):
        return super(CustomAppManager, self).get_queryset().select_related(
            'category',
            'experience',
            'work_schedule',
            'salary_condition',
            'employment_type',
            'location',
        )