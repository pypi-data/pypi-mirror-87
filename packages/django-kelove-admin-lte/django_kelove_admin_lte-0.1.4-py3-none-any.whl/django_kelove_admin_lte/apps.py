"""
apps.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-24 4:43 PM
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoKeloveAdminLteConfig(AppConfig):
    """
    DjangoKeloveAdminLteConfig
    """

    label = 'django_kelove_admin_lte'
    name = 'django_kelove_admin_lte'
    verbose_name = _('AdminLTE3')
