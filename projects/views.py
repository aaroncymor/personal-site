from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectForm
from myportfolio.core.views import ModifiedPaginateListView

# Create your views here.

class ProjectListView(ModifiedPaginateListView):
    model = Project
    paginate_by = 10
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'


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
                    project.rank = post_data['rank']
                    project.save()
                except ValueError:
                    # Error message, update not allowed
                    pass
            else:
                data = {
                    'name': post_data['name'],
                    'description': post_data['description'],
                    # default would always be count + 1
                    'rank': Post.objects.all().count() + 1
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
                    'description': project.description,
                    'rank': project.rank
                })

                context['project_id'] = project.id
            except ValueError:
                # alphabet or special characters not allowed
                pass
        
        if 'prev_page_session' in request_get_keys:
            context['prev_page_session'] = request.GET['prev_page_session']

        context['form'] = form

        return self.render_to_response(context)