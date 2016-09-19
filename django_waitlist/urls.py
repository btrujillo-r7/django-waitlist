from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from django.contrib import admin

from django_waitlist.views import sign_up

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^ping/", TemplateView.as_view(template_name="ping.json"), name="ping"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^waitlist_entries/', include('waitlist_entries.urls', namespace="waitlist_entries")),
    url(r'^vulnerabilities/', include('vulnerabilities.urls', namespace="vulnerabilities")),

    # url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^users/sign_in/$', login, name='login'),
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
