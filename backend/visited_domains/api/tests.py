from django.urls import reverse
from rest_framework.test import APITestCase
from domains.models import Domain
import datetime


class VisitedLinksTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('visited_links')
        self.valid_urls = ['http://example.com', 'https://google.com', 'https://google.com/endpoint']
        self.invalid_urls = ['bad_example.com', '123']
        self.domains = ['example.com', 'google.com']

    def test_post_valid_urls_creates_domain_objects(self):
        data = {'links': self.valid_urls}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что объекты Domain были созданы
        self.assertEqual(Domain.objects.count(), len(self.valid_urls))

        # Проверяем, что имена доменов соответствуют доменам входных URL
        domains = Domain.objects.values_list('name', flat=True)
        self.assertEqual(set(domains), set(self.domains))

    def test_post_invalid_urls_returns_warning(self):
        data = {'links': self.invalid_urls + self.valid_urls}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что объекты были созданы только дял валидных URL
        self.assertEqual(Domain.objects.count(), 3)
        domains = Domain.objects.values_list('name', flat=True)
        self.assertEqual(set(domains), set(self.domains))

        # Проверяем, что невалидные URL есть в ответе
        data = response.json()
        self.assertEqual(data['status'], 'warning')
        self.assertEqual(set(data['invalid_urls']), set(self.invalid_urls))

    def test_post_no_links_returns_error(self):
        data = {}  # Отсутствует ключ 'links'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'No links provided')


class VisitedDomainsTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('visited_domains')
        self.domains = ['example.com', 'google.com']
        Domain.objects.create(name='example.com', created=datetime.datetime(2023, 1, 1))
        Domain.objects.create(name='google.com', created=datetime.datetime(2023, 1, 2))
        Domain.objects.create(name='yandex.ru', created=datetime.datetime(2023, 1, 3))

    def test_get_returns_distinct_domain_names(self):
        Domain.objects.create(name='example.com')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что возвращаются только уникальные домены
        data = response.json()
        self.assertEqual(len(data['domains']), 3)
        self.assertEqual(set(data['domains']), {'example.com', 'google.com', 'yandex.ru'})
        self.assertEqual(data['status'], 'ok')

    def test_get_with_from_param(self):
        response = self.client.get(self.url, data={'from': 1672606800})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(set(data['domains']), {'google.com', 'yandex.ru'})
        self.assertEqual(data['status'], 'ok')

    def test_get_with_to_param(self):
        response = self.client.get(self.url, data={'to': 1672606800})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(set(data['domains']), {'google.com', 'example.com'})
        self.assertEqual(data['status'], 'ok')

    def test_get_with_from_and_to_params(self):
        response = self.client.get(self.url, data={'from': 1672606800, 'to': 1672606800})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(set(data['domains']), {'google.com'})
        self.assertEqual(data['status'], 'ok')