from django import template

register = template.Library()


def paginator(object, get_param):
    return {
        'object': object,
        'get_param': get_param
    }


register.inclusion_tag('templatetags/paginator.html')(paginator)
