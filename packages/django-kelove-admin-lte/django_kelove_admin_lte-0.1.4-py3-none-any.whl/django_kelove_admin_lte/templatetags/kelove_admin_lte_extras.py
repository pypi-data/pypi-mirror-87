"""
kelove_admin_lte_extras.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 2020-08-26 8:28 AM
"""

import re

from django.utils import timezone
from django import template
from django.contrib.admin import DateFieldListFilter
from django.template.loader import get_template

from ..conf import settings

register = template.Library()


@register.simple_tag
def kelove_admin_lte_menu(app_list: list) -> list:
    """
    获取菜单
    :param app_list:
    :return:
    """

    menus = settings.ADMIN_MENUS
    new_app_list = []
    for app in app_list:
        app_info = menus.get(app['app_label'], {})
        if app_info is None:
            continue
        if isinstance(app_info, dict):
            app.update(app_info)
        app['sort'] = app.get('sort', 0)
        models = []
        for model in app['models']:
            model_info = menus.get(app['app_label'] + '.' + model['object_name'], {})
            if model_info is None:
                continue
            if isinstance(model_info, dict):
                model.update(model_info)
            model['sort'] = model.get('sort', 0)
            models.append(model)
            models = sorted(models, key=lambda o: o['sort'], reverse=True)
        app['models'] = models
        new_app_list.append(app)
        new_app_list = sorted(new_app_list, key=lambda o: o['sort'], reverse=True)
    return new_app_list


@register.simple_tag
def kelove_admin_lte_setting(key: str, default=None):
    """
    获取可用配置
    :param key:
    :param default:
    :return:
    """

    return getattr(settings, key, default)


@register.simple_tag
def kelove_admin_lte_filter_type(spec) -> str:
    """
    获取 filter 类型
    :param spec:
    :return:
    """

    if isinstance(spec, DateFieldListFilter):
        return 'DateFieldListFilter'
    else:
        return 'default'


@register.simple_tag
def kelove_admin_lte_list_filter(request, cl, spec):
    """
    重构 admin_list_filter
    :param request:
    :param cl:
    :param spec:
    :return:
    """

    # mtpp 兼容
    if spec.template == 'admin/mptt_filter.html':
        spec.template = 'admin/filter.html'

    tpl = get_template(spec.template)
    return tpl.render({
        'request': request,
        'title': spec.title,
        'choices': list(spec.choices(cl)),
        'spec': spec,
        'cl': cl,
    })


@register.simple_tag
def kelove_admin_lte_get_date_range(request, spec, separator: str = '~') -> str:
    """
    获取时间范围查询的值
    :param request:
    :param spec:
    :param separator:
    :return:
    """

    request_get_data = request.GET
    lookup_kwarg_since_val = request_get_data.get(spec.lookup_kwarg_since, None)
    lookup_kwarg_until_val = request_get_data.get(spec.lookup_kwarg_until, None)
    if lookup_kwarg_since_val and lookup_kwarg_until_val:
        return "{lookup_kwarg_since_val}{separator}{lookup_kwarg_until_val}".format(
            separator=separator,
            lookup_kwarg_since_val=str(lookup_kwarg_since_val),
            lookup_kwarg_until_val=str(lookup_kwarg_until_val),
        )
    else:
        return ''


@register.simple_tag
def kelove_admin_lte_get_timezone() -> str:
    """
    获取当前时区
    :return:
    """

    default_timezone = '+08:00'
    now = str(timezone.localtime())
    pattern = re.compile(r'^.*?\..*?([+-].*?)$')
    result = re.findall(pattern, now)
    if result:
        return result[0]
    else:
        return default_timezone


@register.simple_tag
def kelove_admin_lte_filter_choice(cl, spec, choice: dict) -> dict:
    """
     获取choice mptt 兼容处理
    :param cl:
    :param spec:
    :param choice:
    :return:
    """

    __padding_style = choice.get('padding_style', '')

    if not __padding_style:
        return choice

    __re_pattern = re.compile(r'.*?style.*?:(?P<num>\d+)px.*')
    __num = re.sub(__re_pattern, r'\g<num>', __padding_style)

    if not __num:
        __num = 0

    mptt_level_indent = getattr(cl.model_admin, 'mptt_level_indent', getattr(spec, 'mptt_level_indent', None))

    if not mptt_level_indent:
        return choice

    mptt_level_num = int(__num) // int(mptt_level_indent)
    display = '{}{}'.format(mptt_level_num * '---', choice.get('display', ''))
    choice['display'] = display
    return choice
