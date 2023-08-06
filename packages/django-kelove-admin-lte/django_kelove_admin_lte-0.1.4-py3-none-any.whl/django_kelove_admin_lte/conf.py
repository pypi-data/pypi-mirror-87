"""
conf.py 配置管理
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-26 8:37 AM
"""

from django.conf import settings as django_settings


class Settings:
    """
    This is a simple class to take the place of the global settings object.

    An instance will contain all of our settings as attributes, with default
    values if they are not specified by the configuration.

    """

    defaults: dict = {
        # 是否展示项目链接
        'SHOW_PROJECT_URL': True,
        # 菜单配置
        'ADMIN_MENUS': {
            "core_user": {"icon": "fa fa-fw fa-users-cog"},
            "core_user.User": {"icon": "fa fa-fw fa-user"},
            "auth": {"icon": "fa fa-fw fa-shield-alt"},
            "auth.Group": {"icon": "fa fa-fw fa-users-cog"},
            "auth.Permission": {"icon": "fa fa-fw fa-shield-alt"},
            "auth.User": {"icon": "fa fa-fw fa-user"},
        },
        # favicon地址
        'ADMIN_FAVICON': None,
        # logo地址
        'ADMIN_LOGO': None,
        # avatar地址
        'ADMIN_AVATAR': None,
        # 页脚配置
        'ADMIN_FOOTER': '''
        <div class="float-right d-none d-sm-block">
            <b>Version</b> 3.0.5
        </div>
        <strong>Copyright &copy; 2014-2019 <a href="http://adminlte.io">AdminLTE.io</a>.</strong> All rights
        reserved.
        '''
    }

    prefix: str = 'KELOVE_ADMIN_LTE_'

    def __getattr__(self, name: str):

        true_name = name

        if not true_name.startswith(self.prefix):
            true_name = '{prefix}{name}'.format(prefix=self.prefix, name=name)

        if name in self.defaults:
            setting = getattr(django_settings, true_name, self.defaults[name])
        else:
            setting = getattr(django_settings, name)

        return setting


settings = Settings()
