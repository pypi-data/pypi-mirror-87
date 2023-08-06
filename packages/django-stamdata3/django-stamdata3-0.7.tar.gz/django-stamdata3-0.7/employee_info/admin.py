from django.contrib import admin
from django.db.models import Model
from typing import Type

from employee_info.models import Company, CostCenter, Employment, Organisation, Resource


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['companyCode']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['company', 'resourceId', 'firstName', 'lastName']
    list_filter = ['company']
    readonly_fields = ['manages_list', 'subordinates']


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['company', 'orgId', 'name', 'manager']
    list_filter = ['company']
    # readonly_fields = ['employments']


def value_pair_dict(model: Type[Model], key, value):
    data = model.objects.order_by().values(key, value).distinct()
    values = []
    for element in data:
        values.append((element[key],
                       '%s (%s)' % (element[value], element[key])))
    return values


class EmploymentTypeAdmin(admin.SimpleListFilter):
    title = 'Ansettelsestype'
    parameter_name = 'employmentType'

    def lookups(self, request, model_admin):
        types = Employment.objects.order_by().values('employmentType', 'employmentTypeDescription').distinct()
        values = []
        for employment_type in types:
            values.append((employment_type['employmentType'],
                           '%s (%s)' % (employment_type['employmentTypeDescription'], employment_type['employmentType'])))
        return values

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(employmentType=self.value())
        else:
            return queryset


class PostCodeFilter(admin.SimpleListFilter):
    title = 'Stillingskode'
    parameter_name = 'postCode'

    def lookups(self, request, model_admin):
        return value_pair_dict(Employment, 'postCode', 'postCodeDescription')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(postCode=self.value())
        else:
            return queryset


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ['resource', 'mainPosition', 'workPlace', 'costCenter',
                    'postCodeDescription', 'employmentTypeDescription']
    list_filter = [EmploymentTypeAdmin, PostCodeFilter, 'mainPosition', 'resource__company']


@admin.register(CostCenter)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['description', 'value', 'company']
    list_filter = ['company']
