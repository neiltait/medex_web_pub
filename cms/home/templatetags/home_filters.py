from django import template

register = template.Library()

PAGE_PRESENTER_ITEM_MAX = 7


@register.filter()
def page_range_presenter(index_overview):
    half_range = round(PAGE_PRESENTER_ITEM_MAX / 2)

    if index_overview.page_count <= PAGE_PRESENTER_ITEM_MAX:
        return __page_range_presenter_subrange(index_overview, index_overview.page_range)

    elif index_overview.page_number <= half_range:
        return __page_range_presenter_with_dots_at_end(index_overview)

    elif index_overview.page_count - index_overview.page_number < half_range:
        return __page_range_presenter_with_dots_at_start(index_overview)

    else:
        return __page_range_presenter_with_dots_both_ends(index_overview)


def __page_range_presenter_with_dots_at_end(index_overview):
    return __page_range_presenter_subrange(index_overview, range(0, PAGE_PRESENTER_ITEM_MAX - 2)) + \
           __page_range_presenter_spacer_end(index_overview.page_count)


def __page_range_presenter_with_dots_both_ends(index_overview):
    center_range_diff = round((PAGE_PRESENTER_ITEM_MAX - 4) / 2)
    return __page_range_presenter_spacer_start() + \
           __page_range_presenter_subrange(index_overview,
                                           range(index_overview.page_number - center_range_diff,
                                                 index_overview.page_number + center_range_diff - 1)) + \
           __page_range_presenter_spacer_end(index_overview.page_count)


def __page_range_presenter_with_dots_at_start(index_overview):
    return __page_range_presenter_spacer_start() + \
           __page_range_presenter_subrange(index_overview,
                                           range(index_overview.page_count - PAGE_PRESENTER_ITEM_MAX + 2,
                                                 index_overview.page_count))


def __page_range_presenter_subrange(index_overview, page_range):
    page_items = []
    for i in page_range:
        if i == index_overview.page_number - 1:
            page_items.append({'type': 'active', 'page': i + 1})
        else:
            page_items.append({'type': 'link', 'page': i + 1})
    return page_items


def __page_range_presenter_spacer_end(page_max):
    return [{'type': 'spacer', 'page': page_max - 1}, {'type': 'link', 'page': page_max}]


def __page_range_presenter_spacer_start():
    return [{'type': 'link', 'page': 1}, {'type': 'spacer', 'page': 2}]
