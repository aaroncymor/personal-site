from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth import logout, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from blog.models import Post
from projects.models import Project

from .utils import group_pagination

# Create your views here.

class ModifiedPaginateListView(generic.ListView):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
                if is_empty:
                    raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                        'class_name': self.__class__.__name__,
                        })
        context = self.get_context_data()

        if 'group_num' in request.GET.keys():
            # get page_obj
            if context['is_paginated']:
                page_obj = context['page_obj']
                num_of_pages = page_obj.paginator.num_pages
                group_by = settings.GROUP_BY_PAGINATION
                group_num = int(request.GET.get('group_num', None))
                try:
                    curr_page_range = group_pagination(num_of_pages, 
                                    group_by, group_num)
                    print(curr_page_range)
                except ValueError:
                    print("LOLOMO PASS")
                    pass

        return self.render_to_response(context)    


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


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'myportfolio/dashboard.html'


class LoginView(auth_views.LoginView):
    template_name = 'myportfolio/login.html'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            request.session['authorized'] = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('login')