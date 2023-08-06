from django.contrib.auth.decorators import permission_required
from django.db.models import Model
from django.http import HttpResponseBadRequest, JsonResponse
from typing import Type

from employee_info.models import CostCenter, Function, WorkPlace


def __relation_autocomplete(model: Type[Model], company_code, search_value):
    output = []
    query_set = model.objects.filter(company__companyCode=company_code, value__startswith=search_value)

    for value in query_set:
        output.append({'value': value.value, 'label': '%s %s' % (value.value, value.description)})

    return output


def __autocomplete(request, model: Type[Model], limit=1):
    company_code = request.GET.get('company')
    if not company_code:
        return HttpResponseBadRequest('Company must be specified')
    search = request.GET.get('term')
    if search and len(search) >= limit:
        values = __relation_autocomplete(model, company_code, search)
        return JsonResponse(values, safe=False)
    else:
        return HttpResponseBadRequest('At least %d characters must be provided' % limit)


@permission_required('employee_info.view_cost_center')
def cost_center(request):
    return __autocomplete(request, CostCenter, 2)


@permission_required('employee_info.view_function')
def function(request):
    return __autocomplete(request, Function)


@permission_required('employee_info.view_work_place')
def work_place(request):
    return __autocomplete(request, WorkPlace)
