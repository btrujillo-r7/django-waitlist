import json

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render

from waitlist_entries.models import WaitlistEntry

def search(request):
    if request.method == 'POST':
        return HttpResponseForbidden()

    if None is request.GET.get('q'):
        waitlist_entries = []
    else:
        query = "select * from waitlist_entries_waitlistentry where email = '%s'"  % request.GET.get('q')
        waitlist_entries = WaitlistEntry.objects.raw(query)

    context = {'waitlist_entries': waitlist_entries}
    return render(request, 'vulnerabilities/search.html', context)

def sql_exception(request):
    for p in WaitlistEntry.objects.raw("select * from wailskfdj"):
        print(p)

def send_me_json(request):
    if request.method == 'POST':
        return HttpResponse(
            json.dumps({"success": True}),
            content_type='application/json', status=200)
    else:
        return HttpResponseForbidden()
