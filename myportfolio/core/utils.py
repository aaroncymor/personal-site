from math import ceil

from django.shortcuts import get_object_or_404

from bs4 import BeautifulSoup


def parse_html_content(post_content):
    """[summary]
    
    Arguments:
        html_doc {[type]} -- [description]
    """
    soup = BeautifulSoup(post_content)
    return soup.get_text()

def group_pagination(num_pages, group_by, group_number=1):
    """
    Let's say in our queryset, we have 11 number of pages,
    and we wanted to group them by 3 like so below:

    1. 1 2 3 >
    2. < 4 5 6 >
    3. < 7 8 9 >
    4. < 10 11

    total number of pages / group_by (page range to show) = ceil(answer) # group
    num_of_groups = ceil(num_of_pages / group_by)
    
    we have 4 groups from 11 pages

    4 = ceil(11 / 3)

    now all we need to do is determine the page range with the given group_number
    if  we were given group_number = 2, this would return list if [4, 5, 6]

    To get that, we multiply group_number * group_by, from there we can determine the
    page_range

    Returns:
        list -- list of pages based on the given group number
    """
    num_groups = ceil(num_pages / group_by)
    
    # 6 = 2 * 3
    if group_by <= num_groups:
        res = group_number * group_by
        # list(range((6 + 1) - 3, (6 + 1))) or list(range(4, 7))
        start = (res + 1) - group_by
        stop = res + 1

        if res > num_pages:
            stop = num_pages + 1
    else:
        raise ValueError("Number of groups allowable exceeded.")

    return list(range(start, stop))