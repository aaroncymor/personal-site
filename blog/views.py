import datetime

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, Tag, Decipher
from .forms import PostForm, PostSearchForm

from myportfolio.myportfolioapi.filters import PostFilter
from myportfolio.core.utils import (
    ModifiedListView, load_html_doc,
    get_tags, assign_attr_to_tag,
    append_classes_to_tag, wrap_element,
    replace_element
)

#from myportfolio.core.views import ModifiedPaginateListView

# Create your views here.

class PostListView(ModifiedListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    queryset = Post.published_objects.all()
    filter_class = PostFilter

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.

            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })

        context = self.get_context_data()

        # add form here
        context['form'] = PostSearchForm

        # add tags autocomplete here
        tags_autocomplete = Tag.objects.distinct().values_list('tag', flat=True)
        context['tags_autocomplete'] = convert_list_for_chipauto(tags_autocomplete)

        return self.render_to_response(context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        deciphers = Decipher.objects.filter(post=self.object)
        context['deciphers'] = deciphers

        if 'prev_page_session' in request.GET.keys():
            context['prev_page_session'] = request.GET['prev_page_session']

        return self.render_to_response(context)


class PostFormView(LoginRequiredMixin, generic.FormView):
    login_url = '/login'

    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/blog/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        request_get_keys = request.GET.keys()

        post = None
        if form.is_valid():
            post_data = request.POST.dict()
            # tags from form
            tags = request.POST.getlist('tags')

            try:
                # TODO: Make DateFormat UTC
                post_data['publish']
                published_date = datetime.datetime.now()
            except KeyError:
                published_date = None

            if 'id' in request_get_keys:
                try:
                    post = get_object_or_404(Post, pk=request.GET['id'])
                    
                    if not post:
                        raise Http404

                    # TODO: figure out getting string of html content of returned soup object
                    processed_content = process_decipher_in_post(post, post_data['content'])
                    post.category = Category.objects.get(id=post_data['category_id'])
                    post.title = post_data['title']
                    post.content = processed_content
                    post.published_date = published_date
                    post.save()

                    # tags recorded in database
                    post_tags = post.tags.all().values_list('tag', flat=True)
                    
                    # delete tag in database if tag was removed from form
                    for post_tag in post_tags:
                        if post_tag not in tags:
                            Tag.objects.get(post=post, tag=post_tag).delete()

                    # insert tag if not existing in tags of post
                    for tag in tags:
                        if tag not in post_tags:
                            Tag.objects.create(post=post, tag=tag)
                except ValueError:
                    pass
            else:
                data = {
                    'category_id': post_data['category_id'],
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'published_date': published_date
                }
                temp_content = post_data['content']

                post = Post.objects.create(**data)
                
                # process decipher span
                processed_content = process_decipher_in_post(post, temp_content)
                post.content = processed_content
                post.save()

                post_tags = []
                if tags:
                    for tag in tags:
                        post_tags.append(Tag(post=post, tag=tag))

                Tag.objects.bulk_create(post_tags)
            
        redirect_url = "{0}?id={1}".format(reverse('post-form'), post.id)
        if 'prev_page_session' in request_get_keys:
            redirect_url += '&prev_page_session=' + request.GET['prev_page_session']


        return redirect(redirect_url)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        tags = []
        context = {}
        request_get_keys = request.GET.keys()

        tags_autocomplete = Tag.objects.distinct().values_list('tag', flat=True)

        if 'id' in request_get_keys:
            try:
                post = get_object_or_404(Post, pk=request.GET['id'])
                tags = post.tags_obj

                if not post:
                    raise Http404
                
                form = self.form_class({
                    'category_id': post.category.id,
                    'title': post.title,
                    'content': post.content,
                    'publish': True if post.published_date else False
                })

                context['post_id'] = post.id

            except ValueError:
                pass
        
        if 'prev_page_session' in request_get_keys:
            context['prev_page_session'] = request.GET['prev_page_session']

        context['form'] = form
        context['tags'] = tags
        context['tags_autocomplete'] = convert_list_for_chipauto(tags_autocomplete)

        return self.render_to_response(context)


def submit_post_search(request):
    """Assumes paginated already, hence we use paginate queryset function.
    
    Arguments:
        request {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    context = {'form': PostSearchForm()}
    paginated, page, post_qs, is_paginated = None, None, None, False
    
    if request.method == "POST":
        session_keys = request.session.keys()

        # For each new post request or click of search form,
        # remove session with name (reference: ModifiedListView)
        # filter_class.base_filter + filter_field_suffix
        if 'category_search' in session_keys:
            del request.session['category_search']
        
        if 'title_search' in session_keys:
            del request.session['title_search']
        
        if 'tags_search' in session_keys:
            del request.session['tags_search']

        search_filter = {}
        form = PostSearchForm(request.POST)
        category, title, tags = None, None, None
        if form.is_valid():
            post_data = request.POST.dict()

            category = post_data.get('category', None)
            if category:
                search_filter['category'] = category

            title = post_data.get('title', None)
            if title:
                search_filter['title'] = title

        if 'tags' in request.POST.keys():
            tags = ','.join(request.POST.getlist('tags'))
        
        if not category and not title and not tags:
            return redirect(reverse('post-list'))

        # add sessions for filter fields to cache paginated queryset
        # session name must be in filter_class.base_filter with the item
        # by filter_field_suffix (See ModifiedListView in utils). In this
        # case, it is base_filter + '_search'
        if category:
            search_filter['category_name'] = category
            request.session['category_name_search'] = category
        
        if title:
            search_filter['title'] = title
            request.session['title_search'] = title

        if tags:
            search_filter['tags'] = tags
            request.session['tags_search'] = tags
        
        post_qs = PostFilter(search_filter, 
                             queryset=Post.published_objects.all()).qs

        # TODO: page_size should come from config or settings, not fix size of 10
        paginator, page, queryset, is_paginated = paginate_queryset(request=request,
                                                                    queryset=post_qs,
                                                                    page_size=10)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['is_paginated'] = is_paginated
        context['object_list'] = post_qs
        context['posts'] = post_qs

        # tags auto complete
        tags_autocomplete = Tag.objects.distinct().values_list('tag', flat=True)
        context['tags_autocomplete'] = convert_list_for_chipauto(tags_autocomplete)

    return render(request, 'blog/post_list.html', context)


def delete_post(request, pk):
    if Post.objects.filter(pk=pk).exists():
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect(reverse('post-list'))
    return Http404


def get_random_tags(request):
    # TODO: This view will showcase randomize tags and when you click,
    # it will show the corresponding post.

    context = {}
    if 'tag' in request.GET.keys():
        posts = Post.published_objects.filter(tags__tag=request.GET['tag'])
        context['posts'] = posts
    
    # TODO: we can change how tags we want to appear
    # for now default value of 10.
    from random import choice
    tag_list = Tag.objects.values_list('tag', flat=True).distinct()
    tags = []
    while len(tags) < 10:
        random_tag = choice(tag_list)
        if random_tag not in tags:
            tags.append(random_tag)
        
        if len(tag_list) < 10 and len(tags) == len(tag_list):
            break
    context['tags'] = tags
    return render(request, 'blog/post_random_tags.html', context)


# None view functions
def paginate_queryset(request, queryset, page_size, orphans=0, allow_empty=True, page_kwarg='page'):
    """
    Code coming from the following attributes and methods under ListView CBV.

    attributes: allow_empty, paginate_orphans, paginator_class

    Reference:
    https://ccbv.co.uk/projects/Django/2.1/django.views.generic.list/ListView/
    
    Arguments:
        queryset {[type]} -- [description]
        page_size {[type]} -- [description]
    """
    from django.core.paginator import Paginator

    paginator = Paginator(queryset, page_size, orphans=orphans, allow_empty_first_page=allow_empty)
    page = request.GET.get(page_kwarg) or 1

    try:
        page_number = int(page)
    except ValueError:
        if page == 'last':
            page_number = paginator.num_pages
        else:
            raise Http404(_("Page is not 'last', nor can it be converted to an int."))
    try:
        page = paginator.page(page_number)
        return (paginator, page, page.object_list, page.has_other_pages)
    except InvalidPage as e:
        raise Http404(_('Invalid page (%(page_number)s): %(message)s') %{
            'page_number': page_number,
            'message': str(e)
        })

def convert_list_for_chipauto(item_list):
    # converts list for autocomplete initialization
    # for materialize in this format
    # { 'Microsoft': null, 'Google': null, 'Apple': null}
    autocomplete = {}
    for item in item_list:
        autocomplete[item] = ''
    
    return autocomplete

def process_decipher_in_post(post, post_content):
    ## TODO: Process decipher objects wherein, when deleted,
    ## get id and use that to delete object by id.
    soup = load_html_doc(post_content)

    # will only process div element with class 'decipher'
    deciphers = get_tags(soup, 'span.decipher')

    # decipher ids from content
    content_decipher_ids = []

    # create or update
    if deciphers:
        for decipher in deciphers:
            try:
                decipher_id = int(decipher['id'][11:])

                instance = Decipher.objects.get(id=decipher_id)
                # update decipher
                instance.hidden_text = decipher.string
                instance.save()

                # if id was successfully parsed to int and is
                # existing append to content_decipher_ids list
                # so they would not be deleted later
                content_decipher_ids.append(decipher_id)
            except (KeyError, ValueError, Decipher.DoesNotExist):
                # save decipher to db
                instance = Decipher.objects \
                                        .create(post=post, hidden_text=decipher.string)

                assign_attr_to_tag(
                    tag=decipher,
                    target_attr='id',
                    attr_val='decipherme-' + str(instance.id)
                )

                # also append newly saved decipher's id so
                # it would not be deleted later
                content_decipher_ids.append(instance.id)

    # get existing id of deciphers from given post
    post_decipher_ids = Decipher.objects.filter(post=post).values_list('id', flat=True)

    # delete all deciphers from db that are no longer found
    # on content (from content_decipher_ids)
    for post_decipher_id in post_decipher_ids:
        if post_decipher_id not in content_decipher_ids:
            instance = Decipher.objects.get(id=post_decipher_id)
            instance.delete()

    return soup.prettify(formatter="html5")