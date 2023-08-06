from django.urls import path

from .. import views

app_name = 'employee_info_autocomplete'

urlpatterns = [
    path('cost_center', views.autocomplete.cost_center, name='autocomplete_cost_center'),
    path('function', views.autocomplete.function, name='autocomplete_function'),
    path('work_place', views.autocomplete.work_place, name='autocomplete_work_place')
]
