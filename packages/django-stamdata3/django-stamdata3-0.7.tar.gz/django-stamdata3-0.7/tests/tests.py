import os

from django.test import TestCase

# Create your tests here.
from employee_info.models import Resource, Employment

from employee_info.load_data.load_resources import LoadResources


class ResourceTestCase(TestCase):
    def setUp(self) -> None:
        folder = os.path.dirname(__file__)
        load = LoadResources(os.path.join(folder, 'test_data', 'stamdata_multi.xml'), 'AK')
        load.load()

    def testMainPosition(self):
        resource = Resource.objects.get(resourceId=53453)
        main = resource.main_position()
        self.assertIsInstance(main, Employment)
