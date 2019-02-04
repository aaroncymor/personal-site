from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from .models import Project
from .forms import ProjectForm

# Create your views here.

class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 10
    template_name = 'projects/project_list.html'


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


class ProjectFormView(generic.FormView):
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = '/projects/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            post_data = request.POST.dict()

            if 'id' in request.GET.keys():
                if Project.objects.filter(id=request.GET['id']).exists():
                    project = Project.objects.get(id=request.GET['id'])
                    project.name = post_data['name']
                    project.description = post_data['description']
                    project.save()
            else:
                data = {
                    'name': post_data['name'],
                    'description': post_data['description']
                }
                project = Project.objects.create(**data)
            
        return self.render_to_response({})

    def get(self, request, *args, **kwargs):
        form = self.form_class
        
        if 'id' in request.GET.keys():
            project = get_object_or_404(Project, pk=request.GET.get('id'))
            form = self.form_class({
                'name': project.name,
                'description': project.description
            })
        return self.render_to_response({'form': form})