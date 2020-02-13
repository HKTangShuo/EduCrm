from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import URLResolver, URLPattern  # 用于判断url类型
import re


def check_url_exclude(url):
    """白名单"""  # 写配置文件里面
    exclude_url = settings.AUTO_DISCOVER_EXCLUDE
    for regex in exclude_url:
        if re.match(regex, url):
            return True


def get_all_url_dict():
    # 获取项目中所有url,必须有name别名
    url_ordered_dict = OrderedDict()
    """
    {
        "rbac:menu_list":{'name':'rbac:menu_list','url':'xxx/xxxx/menu/list'}
    }

    """
    root_url = import_string(settings.ROOT_URLCONF)
    recursion_urls(
        pre_namespace=None,
        pre_url='/',
        urlpatterns=root_url.urlpatterns,
        url_ordered_dict=url_ordered_dict)

    return url_ordered_dict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """

    :param pre_namespace: namespace的前缀，以后用于拼接name
    :param pre_url: url前缀，用于拼接url
    :param urlpatterns: 循环的路由
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """

    for item in urlpatterns:
        if isinstance(item, URLPattern):
            # 已经找到最后一级，添加到字典中
            if not item.name:
                continue
            # name有前缀就拼接 没前缀就直接name
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name
            # url有没有前缀，
            url = pre_url + item.pattern.regex.pattern  # 拼接url，去掉^和$
            url = url.replace("^", "").replace("$", "")
            if check_url_exclude(url):  # 白名单
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(
                namespace,
                pre_url +
                item.pattern.regex.pattern,
                item.url_patterns,
                url_ordered_dict)
            # 接着找，递归
            pass
