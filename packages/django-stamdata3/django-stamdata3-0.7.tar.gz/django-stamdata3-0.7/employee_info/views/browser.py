from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

from employee_info.models import Resource, Company, Organisation


def index(request):
    return render(request, 'employee_info/index.html', {'companies': Company.objects.all()})


@permission_required('employee_info.view_employment')
def resource(request):
    employee_num = request.GET.get('employee')
    if not employee_num:
        employee_num = request.GET.get('value')

    company = request.GET.get('company')

    if employee_num:
        resource_obj = Resource.objects.get(company__companyCode=company,
                                            resourceId=employee_num)
        return render(request, 'employee_info/resource.html',
                      {'resource': resource_obj,
                       'title': 'Ansatt',
                       'companies': Company.objects.all()})
    else:
        return redirect('employee_info_browser:index')


@permission_required('employee_info.view_organisation')
def organisation(request):
    company = request.GET.get('company')
    organisation_num = request.GET.get('value')
    if not company:
        return render(request, 'employee_info/select_company.html', {'title': 'Velg firma',
                                                                     'companies': Company.objects.all()
                                                                     })
    elif not organisation_num:
        return render(request, 'employee_info/select_organisation.html',
                      {'title': 'Velg organisasjonsenhet',
                       'organisations': Organisation.objects.filter(company__companyCode=company),
                       'company': company})

    organisation_obj = Organisation.objects.get(company__companyCode=company, orgId=organisation_num)
    return render(request, 'employee_info/organisation.html', {'organisation': organisation_obj, 'company': company})
