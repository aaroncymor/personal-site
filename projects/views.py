from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectForm
from myportfolio.core.views import ModifiedPaginateListView

# Create your views here.

class ProjectListView(ModifiedPaginateListView):
    model = Project
    paginate_by = 10
    template_name = 'projects/project_list.html'


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


class ProjectFormView(LoginRequiredMixin, generic.FormView):
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = '/projects/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            post_data = request.POST.dict()

            if 'id' in request.GET.keys():
                try:
                    project = get_object_or_404(Project, pk=request.GET.get('id'))
                    
                    if not project:
                        raise Http404

                    project = Project.objects.get(id=request.GET['id'])
                    project.name = post_data['name']
                    project.description = post_data['description']
                    project.save()
                except ValueError:
                    # Error message, update not allowed
                    pass
            else:
                data = {
                    'name': post_data['name'],
                    'description': post_data['description']
                }
                project = Project.objects.create(**data)
            
        return self.render_to_response({'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class
        
        if 'id' in request.GET.keys():
            try:
                project = get_object_or_404(Project, pk=request.GET.get('id'))
                
                if not project:
                    raise Http404

                form = self.form_class({
                    'name': project.name,
                    'description': project.description
                })
            except ValueError:
                # alphabet or special characters not allowed
                pass

        return self.render_to_response({'form': form})