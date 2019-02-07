import datetime

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Post, Category, Tag
from .forms import PostForm

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostFormView(LoginRequiredMixin, generic.FormView):
    login_url = '/login'

    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/blog/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        post = None
        if form.is_valid():
            post_data = request.POST.dict()
            tags = request.POST.getlist('tags')

            try:
                # TODO: Make DateFormat UTC
                post_data['publish']
                published_date = datetime.datetime.now()
            except KeyError:
                published_date = None

            if 'id' in request.GET.keys():
                try:
                    post = get_object_or_404(Post, pk=request.GET['id'])
                    
                    if not post:
                        raise Http404

                    post.category = Category.objects.get(id=post_data['category_id'])
                    post.title = post_data['title']
                    post.content = post_data['content']
                    post.published_date = published_date
                    post.save()

                    post_tags = post.tag_set.all().values_list('tag', flat=True)
                    
                    # delete if tag was removed from form POST
                    for post_tag in post_tags:
                        if post_tag not in tags:
                            tag = Tag.objects.get(post=post, tag=post_tag)
                            tag.delete()

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
                post = Post.objects.create(**data)

                post_tags = []
                if tags:
                    for tag in tags:
                        post_tags.append(Tag(post=post, tag=tag))

                Tag.objects.bulk_create(post_tags)

        return redirect("{0}?id={1}".format(reverse('post-form'), post.id))

    def get(self, request, *args, **kwargs):
        form = self.form_class
        tags = []
        context = {}
        if 'id' in request.GET.keys():
            try:
                post = get_object_or_404(Post, pk=request.GET['id'])
                tags = post.tags

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

        context['form'] = form
        context['tags'] = tags

        return self.render_to_response(context)

