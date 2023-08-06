from django.db import IntegrityError
from django.db.models import ProtectedError
from stamdata3.exceptions import InvalidRelation
from .load_data import LoadData
from ..models import Resource, Employment, Function, CostCenter, WorkPlace, Organisation
from stamdata3.Resource import Resource as Resource_stamdata


class LoadResources(LoadData):
    def load(self):
        orphans = Resource.objects.filter(company__companyCode=self.company_code)
        resources = self.stamdata.resources()
        for resource in resources:
            if resource.company_code != self.company_code:
                raise ValueError('Company code %s in file, %s requested' % (resource.company_code, self.company_code))
            resource_obj, created = Resource.objects.get_or_create(
                company=self.company,
                resourceId=resource.resource_id)

            resource_obj.firstName = resource.first_name
            resource_obj.lastName = resource.last_name
            resource_obj.socialSecurityNumber = resource.ssn
            resource_obj.status = resource.status

            resource_obj.save()
            orphans = orphans.exclude(id=resource_obj.id)

            self.load_employments(resource, resource_obj)
        for orphan in orphans:
            try:
                orphan.delete()
            except ProtectedError:
                print('Protected relations: %s' % orphan)
            except IntegrityError as e:
                print('Error deleting %s: %s' % (orphan, e))

    def load_employments(self, resource: Resource_stamdata, resource_obj: Resource):
        for employment in resource.employments:
            try:
                emp = Employment.objects.get(resource=resource_obj, id=employment.sequence_ref)
            except Employment.DoesNotExist:
                emp = Employment(resource=resource_obj, id=employment.sequence_ref)

            emp.employmentType = employment.type
            emp.employmentTypeDescription = employment.type_description
            emp.mainPosition = employment.main_position
            emp.percentage = employment.percentage
            emp.postId = employment.post_id
            emp.postIdDescription = employment.post_id_description
            emp.postCode = employment.post_code
            emp.postCodeDescription = employment.post_code_description

            try:
                emp.function = self.load_function(employment)
            except InvalidRelation as e:
                print(e)

            try:
                emp.costCenter = self.load_cost_center(employment)
            except InvalidRelation as e:
                print(e)

            try:
                emp.workPlace = self.load_work_place(employment)
            except InvalidRelation:
                pass

            try:
                emp.organisation = self.load_organisation(employment)
            except InvalidRelation as e:
                print(e)

            emp.dateFrom = employment.date_from
            emp.dateTo = employment.date_to
            emp.save()

    def load_function(self, employment):
        function = employment.relation('FUNCTION')
        function, created = Function.objects.get_or_create(company=self.company, value=function.value,
                                                           defaults={'description': function.description})
        return function

    def load_cost_center(self, employment):
        relation = employment.relation('COST_CENTER')
        cost_center, created = CostCenter.objects.get_or_create(
            company=self.company,
            value=relation.value,
            defaults={'description': relation.description})
        return cost_center

    def load_work_place(self, employment):
        relation = employment.relation('WORK_PLACE')
        workplace, created = WorkPlace.objects.get_or_create(
            company=self.company,
            value=relation.value,
            defaults={'description': relation.description})
        return workplace

    def load_organisation(self, employment):
        relation = employment.relation('ORGANIZATIONAL_UNIT')
        try:
            return Organisation.objects.get(
                company=self.company,
                orgId=relation.value)

        except Organisation.DoesNotExist:
            print('Organisation %s does not exist' % relation.value)
