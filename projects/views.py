from django.shortcuts import render
from django.views import generic, View

from .models import Project

# Create your views here.

class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 10
    template_name = 'projects/project_list.html'


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'