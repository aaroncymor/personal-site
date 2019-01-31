from django.shortcuts import render
from django.views import generic

from blog.models import Post
from projects.models import Project

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Queryset for blogs - latest three (3) posts
        posts = Post.objects.all().order_by('-timestamp')[:3]

        # Queryset for projects - latest three (3) projects
        projects = Project.objects.all().order_by('-timestamp')[:3]

        # Assign to context
        context['posts'] = posts
        context['projects'] = projects

        return self.render_to_response(context)

