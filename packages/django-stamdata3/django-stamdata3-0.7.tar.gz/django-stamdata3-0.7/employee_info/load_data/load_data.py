from employee_info.models import Company
from stamdata3.stamdata3 import Stamdata3


class LoadData:
    def __init__(self, file, company_code):
        self.company_code = company_code
        self.stamdata = Stamdata3(file)
        self.company, created = Company.objects.get_or_create(
            companyCode=company_code)
