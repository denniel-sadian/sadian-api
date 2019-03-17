from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Project
from .models import Day
from .models import AboutMe
from .models import Timeline


def get_categories():
    categories = []
    for project in Project.objects.all():
        if project.category not in categories:
            categories.append(project.category)
    return categories


def get_day_year_week():
    day = Day.objects.get(id=timezone.datetime.now().isoweekday())
    year = timezone.datetime.now().year
    week = timezone.datetime.now().strftime('%A')
    return day, year, week


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
        extra['category'] = project_category

        paginator = Paginator(queryset.all(), 12)
        self.extra_context = extra
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting the project categories
        context['categories'] = get_categories()

        # getting the day, year and week
        context['day'], context['year'], context['week'] = get_day_year_week()

        return context


class ProjectDetailView(generic.DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting the project categories
        context['categories'] = get_categories()

        # setting the current category
        context['category'] = self.object.category

        # getting the day, year and week
        context['day'], context['year'], context['week'] = get_day_year_week()

        return context


class AboutMeListView(generic.ListView):
    queryset = AboutMe.objects.all()
    context_object_name = 'paragraphs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting the project categories
        context['categories'] = get_categories()

        #getting timelines
        context['timelines'] = Timeline.objects.all()

        # getting the day, year and week
        context['day'], context['year'], context['week'] = get_day_year_week()

        return context
