from django.test import TestCase, Client
from django.urls import reverse


class URLTests(TestCase):

    def test_courses_list_view(self):
        c = Client()
        status_code = c.get(reverse('course:list')).status_code
        self.assertEqual(status_code, 200)
