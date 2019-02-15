from math import ceil

from django.conf import settings
from django.views import generic
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet


from bs4 import BeautifulSoup

def parse_html_content(post_content):
    """[summary]
    
    Arguments:
        html_doc {[type]} -- [description]
    """
    soup = BeautifulSoup(post_content)
    return soup.get_text()

def enum(sequence, start=0):
    for index, value in enumerate(sequence):
        yield index + start, value

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
    group_page_next, group_page_prev = None, None

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

    # check if given group_num is within num_groups
    # and calculate new start and stop value
    if group_num <= num_groups and group_num > 0:
        res = group_num * group_by
        # list(range((6 + 1) - 3, (6 + 1))) or list(range(4, 7))
        start = (res + 1) - group_by
        stop = res + 1

        if res > num_pages:
            stop = num_pages + 1

    page_list = list(range(start, stop))

    # check if has_next group
    if group_num < num_groups and group_num > 0:
        has_next = True
        next_num = group_num + 1
        group_page_next = page_list[len(page_list) - 1] + 1
    
    # check if has_prev group
    if group_num > 1 and group_num <= num_groups:
        has_prev = True
        prev_num = group_num - 1
        group_page_prev = page_list[0] - 1
    
    grouped_pagination = {
        'grouped_pagination': page_list,
        'group_has_next': has_next,
        'group_has_prev': has_prev,
        'group_next': next_num,
        'group_prev': prev_num,
        'group_page_next': group_page_next,
        'group_page_prev': group_page_prev,
        'group_curr': group_num,
    }

    return grouped_pagination


class ModifiedListView(generic.ListView):
    filter_class = None
    filter_fields = []
    filter_field_suffix = '_search'

    def get_filter_class(self):
        return self.filter_class
    
    def get_filter_fields(self):
        return self.filter_fields

    def get_filter_suffix(self):
        return self.filter_field_suffix

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        
        -Aaron overriding get_queryset for pagination with filters
        https://github.com/django/django/blob/2.1/django/views/generic/list.py#L194
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        # Adding filter to queryset
        filter_class = self.get_filter_class()
        search_filter = {}

        if self.request.session and self.filter_class:
            session_keys = self.request.session.keys()
            if self.filter_fields:
                for base_filter in self.filter_class.base_filters.keys():
                    search_filter_field = base_filter + self.get_filter_suffix()
                    if search_filter_field in session_keys:
                        search_filter[base_filter] = self.request.session[search_filter_field]
                queryset = self.filter_class(search_filter, queryset=queryset).qs
        # End of adding filter queryset

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset    
