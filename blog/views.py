from requests import post

from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Entry, Comment
from .forms import CommentForm
from personal.views import get_day_year_week

from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


class EntryListView(generic.ListView):
    context_object_name = 'entries'

    def get_queryset(self):
        searched = self.request.GET.get('q')
        if searched:
            self.template_name = 'blog/searched.html'
            page = self.request.GET.get('page')
            entries = Entry.objects.filter(status='PB',
                                           headline__icontains=searched).order_by('-pub_date')
            paginator = Paginator(entries.all(), 5)
            self.extra_context = {
                'how_many_found': entries.count(), 'searched': searched}
            return paginator.get_page(page)
        return Entry.objects.filter(status='PB')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # getting the day, year and week
        context['day'], context['year'], context['week'] = get_day_year_week()
        return context


class EntryDetailView(generic.DetailView):
    context_object_name = 'entry'
    template_name = 'blog/entry_detail.html'
    model = Entry
    object = model

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, status='PB', pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # getting the day, year and week
        context['day'], context['year'], context['week'] = get_day_year_week()
        # comments
        all_comments = self.object.comment_set.all()
        paginator = Paginator(all_comments, 10)
        page = self.request.GET.get('page')
        if page:
            comments = paginator.get_page(page)
        else:
            comments = paginator.get_page(paginator.num_pages)
        context['comments'] = comments
        context['true_comment_count'] = all_comments.count()
        return context

    def post(self, request, pk):
        form = CommentForm(request.POST)
        entry = Entry.objects.get(id=pk)
        self.object = entry
        if entry.can_comment and form.is_valid():
            form = form.cleaned_data
            post(f'https://dsadian.herokuapp.com/blog/api/entries/{pk}/comments/',
                 data={
                     'full_name': form['full_name'],
                     'email': form['email'],
                     'content': form['content']
                 })
        return HttpResponseRedirect(f'/blog/detail/{entry.id}/#commentSection')


def my_custom_page_not_found_view(request):
    return render(request, '404.html')
