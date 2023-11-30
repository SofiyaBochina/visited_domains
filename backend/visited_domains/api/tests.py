from django.urls import reverse
from rest_framework.test import APITestCase
from domains.models import Domain


class DomainAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('visited_links')
        self.valid_urls = ['http://example.com', 'https://google.com', 'https://google.com/endpoint']
        self.invalid_urls = ['bad_example.com', '123']
        self.domains = ['example.com', 'google.com']

    def test_get_returns_distinct_domain_names(self):
        Domain.objects.create(name='example.com')
        Domain.objects.create(name='google.com')
        Domain.objects.create(name='google.com')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что возвращаются только уникальные домены
        data = response.json()
        self.assertEqual(set(data['domains']), set(self.domains))
        self.assertEqual(data['status'], 'ok')

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
