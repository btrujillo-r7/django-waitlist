import json

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from django.views.decorators.csrf import csrf_exempt

from waitlist_entries.models import WaitlistEntry

from waitlist_entries.forms import WaitlistEntryForm


def index(request):
    if request.method == 'POST':
        waitlist_entry_form = WaitlistEntryForm(request.POST)

        if waitlist_entry_form.is_valid():
            email = waitlist_entry_form.cleaned_data['email']
            WaitlistEntry.objects.create(email=email)
            redirect(reverse('waitlist_entries:index'))

    else:
        waitlist_entry_form = WaitlistEntryForm()

    waitlist_entries = WaitlistEntry.objects.all()
    context = {
        'waitlist_entries': waitlist_entries,
        'waitlist_entry_form': waitlist_entry_form
    }
    return render(request, 'waitlist_entries/index.html', context)

@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = request.POST

        if not data:
            try:
                data = json.loads(request.body)
            except Exception as e:
                print("Error parsing request body: {e}".format(e=e))

        waitlist_entry_form = WaitlistEntryForm(data)

        if waitlist_entry_form.is_valid():
            email = waitlist_entry_form.cleaned_data['email']
            waitlist_entry = WaitlistEntry.objects.create(email=email)
            return HttpResponse(
                json.dumps({"id": waitlist_entry.id, "email": waitlist_entry.email}),
                content_type='application/json')
        else:
            return HttpResponse(waitlist_entry_form.errors.as_json(), content_type='application/json')

    else:
        return HttpResponseBadRequest()
