from datetime import datetime

from django.core.management.base import BaseCommand
from employee_info.models import Company

from employee_info.load_data.LoadOrganisations import LoadOrganisations

now = datetime.now()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('company', nargs='+', type=str)

    def handle(self, *args, **options):
        company = options['company'][0]
        if company == 'all':
            companies = Company.objects.all()
            companies = list(companies.values_list('companyCode', flat=True))
        else:
            companies = [company]

        for company_code in companies:
            file = '/home/datagrunnlag/Stamdata3_teis_%s.xml' % company_code

            load = LoadOrganisations(file, company_code)
            load.load()
