from blog.models import *
from personal.models import *
from requests import get
from json import loads

entries = loads(get('https://denniel.herokuapp.com/blog/api/entries/').content)
projects = loads(get('https://denniel.herokuapp.com/api/projects/').content)


for p in projects:
    Project.objects.create(
        name=p['name'],
        category=p['category'],
        language_used=p['language_used'],
        image=p['image'],
        date_created=p['date_created'],
        link=p['link'],
        description=p['description']
    )

for e in entries:
    Entry.objects.create(
        headline=e['headline'],
        pub_date=e['pub_date'],
        status=e['status'],
        can_comment=e['can_comment'],
        image=e['image'],
        content=e['content'],
        preview_content=e['preview_content']
    )