from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View

from .models import Post
from .forms import PostForm

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostFormView(View):
    form_class = PostForm
    initial = {}
    template_name = 'blog/post_form.html'