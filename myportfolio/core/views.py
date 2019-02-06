from django.shortcuts import render
from django.views import generic
from django.contrib.auth import views as auth_views

from blog.models import Post
from projects.models import Project

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Queryset for blogs - latest two (2) posts
        posts = Post.published_objects.all().order_by('-timestamp')[:2]

        # Queryset for projects - latest two (2) projects
        projects = Project.objects.all().order_by('-timestamp')[:2]

        # Assign to context
        context['posts'] = posts
        context['projects'] = projects

        return self.render_to_response(context)


class DashboardView(generic.TemplateView):
    template_name = 'myportfolio/dashboard.html'