from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url

from django_waitlist.forms import UserForm

def path_param(request):
    context = {'is_registered': True, 'user_form': UserForm()}
    return render(request, 'registration/register.html', context)

def sign_up(request):
    is_registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            is_registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    context = {'is_registered': is_registered, 'user_form': user_form}

    return render(request, 'registration/register.html', context)

@sensitive_post_parameters()
@csrf_exempt
@never_cache
def sign_in(request,
            _='registration/login.html',
            redirect_field_name=REDIRECT_FIELD_NAME,
            authentication_form=AuthenticationForm,
            __=None):

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        context = {}
        return render(request, 'registration/login.html', context)


import cStringIO as StringIO
import csv
from django.http import StreamingHttpResponse
def big_transfer(request):
    def stream():
        buffer_ = StringIO.StringIO()
        writer = csv.writer(buffer_)

        for i in range(5000):
            row = ",".join(map(str, range(100)))
            writer.writerow(row)
            buffer_.seek(0)
            data = buffer_.read()
            buffer_.seek(0)
            buffer_.truncate()
            yield data

    response = StreamingHttpResponse(
        stream(), content_type='text/csv'
    )
    disposition = "attachment; filename=file.csv"
    response['Content-Disposition'] = disposition
    return response
