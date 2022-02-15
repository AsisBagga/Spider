from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.crawler_url = reverse('crawler')
        self.user_data = {
            'base_url': 'abc.com/xyz',
            'depth': 1,
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
