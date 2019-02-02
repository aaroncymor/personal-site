import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.urls import reverse

from .models import Post, Category
from .forms import PostForm

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostFormView(generic.FormView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/blog/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = None
        if form.is_valid():
            post_data = request.POST.dict()

            try:
                # TODO: Make DateFormat UTC
                post_data['publish']
                published_date = datetime.datetime.now()
            except KeyError:
                published_date = None

            if 'id' in request.GET.keys():
                if Post.objects.filter(id=request.GET['id']).exists():
                    post = Post.objects.get(id=request.GET['id'])
                    post.category = Category.objects.get(id=post_data['category_id'])
                    post.title = post_data['title']
                    post.content = post_data['content']
                    post.published_date = published_date
                    post.save()
            else:
                data = {
                    'category_id': post_data['category_id'],
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'published_date': published_date
                }
                post = Post.objects.create(**data)

        return self.render_to_response({})

    def get(self, request, *args, **kwargs):
        form = self.form_class

        if 'id' in request.GET.keys():
            post = get_object_or_404(Post, pk=request.GET.get('id'))
            form = self.form_class({
                'category': post.category.id,
                'title': post.title,
                'content': post.content,
                'publish': True if post.published_date else False
            })

        return self.render_to_response({'form': form})

