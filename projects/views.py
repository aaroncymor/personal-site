from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectForm

from myportfolio.core.utils import enum, ModifiedSearchListView

# Create your views here.

class ProjectListView(ModifiedSearchListView):
    model = Project
    paginate_by = 10
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    queryset = Project.objects.all().order_by('rank')


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if 'prev_page_session' in request.GET.keys():
            context['prev_page_session'] = request.GET['prev_page_session']
        
        return self.render_to_response(context)


class ProjectFormView(LoginRequiredMixin, generic.FormView):
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = '/projects/'
    queryset = Project.objects \
        .exclude(rank=0) \
        .exclude(rank__isnull=True) \
        .order_by('-rank')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        request_get_keys = request.GET.keys()
        
        if form.is_valid():
            post_data = request.POST.dict()

            if 'id' in request_get_keys:
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
                    'description': post_data['description'],
                    # default would always be count + 1
                    'rank': Project.objects.all().count() + 1
                }
                project = Project.objects.create(**data)

        redirect_url = "{0}?id={1}".format(reverse('project-form'), project.id)
        if 'prev_page_session' in request_get_keys:
            redirect_url += '&prev_page_session=' + request.GET['prev_page_session']
        
        return redirect(redirect_url)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {}
        request_get_keys = request.GET.keys()
        
        if 'id' in request_get_keys:
            try:
                project = get_object_or_404(Project, pk=request.GET.get('id'))
                
                if not project:
                    raise Http404

                form = self.form_class({
                    'name': project.name,
                    'description': project.description
                })

                context['project_id'] = project.id
            except ValueError:
                # alphabet or special characters not allowed
                pass
        
        if 'prev_page_session' in request_get_keys:
            context['prev_page_session'] = request.GET['prev_page_session']

        context['form'] = form

        return self.render_to_response(context)


def delete_project(request, pk):
    if Project.objects.filter(pk=pk).exists():
        project = Project.objects.get(pk=pk)
        temp_rank = project.rank
        project.delete()

        # update rankings
        projects = Project.objects.filter(rank__gt=temp_rank).order_by('rank')
        for i, proj in enumerate(projects):
            proj.rank = temp_rank + i
            proj.save()
        return redirect(reverse('project-list'))
    return Http404s


def get_project_rankings(request):
    context = {}
    projects = Project.objects.all().order_by('rank')
    
    context['projects'] = projects

    return render(request, 'projects/project_rank_form.html', context)


def update_project_rankings(request):
    if request.method == "POST":
        if 'ranks' in request.POST.keys():
            project_ids = request.POST.getlist('ranks')
            for index, value in enum(sequence=project_ids, start=1):
                project = Project.objects.get(id=value)
                project.rank = index
                project.save()

    return redirect(reverse('project-rank-list'))