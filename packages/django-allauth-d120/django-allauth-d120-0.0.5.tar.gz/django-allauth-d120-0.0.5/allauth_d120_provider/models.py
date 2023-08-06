from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext as _


class GroupSync(models.Model):
    external_group = models.CharField(max_length=100, verbose_name=_("External group name"))
    django_group = models.ForeignKey(Group, verbose_name=_("Django Group"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Group synchronization")
        verbose_name_plural = _("Group synchronizations")
        unique_together = ['external_group', 'django_group']

    def __str__(self):
        return "{} -> {}".format(self.external_group, self.django_group)
