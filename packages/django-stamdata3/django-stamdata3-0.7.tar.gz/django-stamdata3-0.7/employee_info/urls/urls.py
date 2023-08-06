from django.urls import include, path

app_name = 'employee_info'

urlpatterns = [
    path('autocomplete/', include('employee_info.urls.autocomplete')),
    path('browser/', include('employee_info.urls.browser'))
]
