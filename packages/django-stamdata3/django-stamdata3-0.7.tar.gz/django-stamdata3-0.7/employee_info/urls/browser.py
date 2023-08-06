from django.urls import path

from ..views import browser as views

app_name = 'employee_info_browser'

urlpatterns = [
    path('', views.index, name='index'),
    path('resource', views.resource, name='resource'),
    path('organisation', views.organisation, name='organisation'),
]
