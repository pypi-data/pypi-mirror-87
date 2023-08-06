from stamdata3.exceptions import InvalidField
from .load_data import LoadData
from ..models import Organisation, Resource


class LoadOrganisations(LoadData):
    def load(self):
        organisations = self.stamdata.organisations()
        for organisation in organisations:
            org, created = Organisation.objects.get_or_create(
                company=self.company,
                orgId=organisation.id
            )

            org.name = organisation.name
            org.status = organisation.status

            if organisation.parent_id is not None:
                try:
                    org.parent = Organisation.objects.get(
                        company=self.company,
                        orgId=organisation.parent_id)
                except Organisation.DoesNotExist:
                    print('Parent organisation %s for %s not found' %
                          (organisation.parent_id, organisation.id))
            else:
                print('%s has no parent organisation' % organisation.id)

            try:
                org.manager = Resource.objects.get(
                    resourceId=organisation.manager,
                    company=self.company
                )
            except Resource.DoesNotExist:
                print('Manager %d not found' % organisation.manager)
            except InvalidField:
                print('No manager for %s' % organisation.id)

            org.save()
