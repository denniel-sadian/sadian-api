from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Project
from .models import AboutMe
from .models import Timeline


class ProjectListView(generic.ListView):
    context_object_name = 'projects'
    template_name = 'personal/project_list.html'

    def get_queryset(self):
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('q')
        page = self.request.GET.get('page')
        queryset = Project.objects
        project_category = ''
        extra = {}

        # for category selection
        if category:
            project_category = category
            queryset = queryset.filter(category__icontains=category.lower())
        # for searching
        elif search_query:
            extra['searched'] = search_query
            queryset = queryset.filter(name__icontains=search_query)

        # extra context
        if not project_category:
            project_category = 'all'
        extra['how_many_really'] = queryset.count()
        extra['current_category'] = project_category

        paginator = Paginator(queryset.all(), 12)
        self.extra_context = extra
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectDetailView(generic.DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # setting the current category
        context['current_category'] = self.object.category

        return context


class AboutMeListView(generic.ListView):
    queryset = AboutMe.objects.all()
    context_object_name = 'paragraphs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting timelines
        context['timelines'] = Timeline.objects.all().order_by('-date')

        return context
