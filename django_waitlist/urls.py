from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.views import (
    logout, password_change, password_change_done, password_reset,
    password_reset_done, password_reset_confirm, password_reset_complete,
)
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin

from django_waitlist.views import sign_up, sign_in, big_transfer, path_param

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^ping/", TemplateView.as_view(template_name="ping.json"), name="ping"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^send_me_elsewhere/$', RedirectView.as_view(url='http://google.com/'), name='send_me_elsewhere'),
    url(r'^waitlist_entries/', include('waitlist_entries.urls', namespace="waitlist_entries")),
    url(r'^vulnerabilities/', include('vulnerabilities.urls', namespace="vulnerabilities")),

    # url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^users/sign_in/$', sign_in, name='login'),
    url(r'^users/sign_out/$', logout, name='logout'),
    url(r'^users/sign_up/$', sign_up, name='register'),
    url(r'^users/password_change/$', password_change, name='password_change'),
    url(r'^users/password_change/done/$', password_change_done, name='password_change_done'),
    url(r'^users/password_reset/$', password_reset, name='password_reset'),
    url(r'^users/password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^users/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^users/reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^big_transfer/$', big_transfer, name='big_transfer'),
    url(r'^path_param/.+$', path_param, name='path_param'),
]

urlpatterns += [url(r'^number_' + str(i) + '/$', TemplateView.as_view(template_name="homepage.html"), name="home") for i in range(1, 1000)]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
