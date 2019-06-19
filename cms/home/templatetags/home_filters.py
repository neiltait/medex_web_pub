from django import template

register = template.Library()


@register.filter()
def page_range_presenter(index_overview):
    PAGE_MAX = 7

    page_range = []

    for i in index_overview.page_range:
        if i == index_overview.page_number - 1:
            page_range.append({'type': 'active', 'page': i+1})
        elif i == 1:
            page_range.append({'type': 'spacer', 'page': i + 1})
        else:
            page_range.append({'type': 'link', 'page': i + 1})

    return page_range
