from math import ceil

from django.conf import settings

from bs4 import BeautifulSoup

def parse_html_content(post_content):
    """[summary]
    
    Arguments:
        html_doc {[type]} -- [description]
    """
    soup = BeautifulSoup(post_content)
    return soup.get_text()

def group_pagination(num_pages, group_num):
    """
    Let's say in our queryset, we have 11 number of pages,
    and we wanted to group them by 3 like so below:

    1. 1 2 3 >
    2. < 4 5 6 >
    3. < 7 8 9 >
    4. < 10 11

    total number of pages / group_by (page range to show) = ceil(answer) # group
    num_of_groups = ceil(num_of_pages / group_by)
    
    We have 4 groups from 11 pages

    4 = ceil(11 / 3)

    Now all we need to do is determine the page range with the given group_number
    if  we were given group_number = 2, this would return list if [4, 5, 6]

    To get that, we multiply group_number * group_by, from there we can determine the
    page_range

    Returns:
        list -- list of pages based on the given group number
    """
    group_by = settings.GROUPBY_PAGINATION

    has_next, has_prev, next_num, prev_num = False, False, None, None

    # default would be group by 1 at group number 0
    num_groups = ceil(num_pages / group_by) if group_by > 0 else num_pages
    start, stop = 1, num_groups + 1

    # if given group_num is more than the
    # determined number of groups, set a default
    # value for it which is 1. This will give
    # default value of group number 1 to process
    # group pagination.
    if group_num > num_groups or group_num < 0:
        group_num = 1

    # check if has_next group
    if group_num < num_groups and group_num > 0:
        has_next = True
        next_num = group_num + 1
    
    # check if has_prev group
    if group_num > 1 and group_num <= num_groups:
        has_prev = True
        prev_num = group_num - 1

    # check if given group_num is within num_groups
    # and calculate new start and stop value
    if group_num <= num_groups and group_num > 0:
        res = group_num * group_by
        # list(range((6 + 1) - 3, (6 + 1))) or list(range(4, 7))
        start = (res + 1) - group_by
        stop = res + 1

        if res > num_pages:
            stop = num_pages + 1
    
    grouped_pagination = {
        'grouped_pagination': list(range(start, stop)),
        'group_has_next': has_next,
        'group_has_prev': has_prev,
        'group_next': next_num,
        'group_prev': prev_num
    }
    print("GROUP PAGINATION DETAILS", grouped_pagination)
    return grouped_pagination