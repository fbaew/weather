from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/?$',views.images, name='images'),
    url(r'^radar/(?P<year>[0-9][0-9][0-9][0-9])/$',views.yearly_radar,name="yearly_radar"),
    url(r'^radar/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$'
        ,views.daily_radar
        ,name="daily_radar"),
]
