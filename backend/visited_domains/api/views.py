from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import urlparse
from rest_framework import status, generics
from rest_framework.response import Response
from domains.models import Domain
from .serializers import DomainSerializer
from .filters import UnixDateFilter


class DomainAPIView(generics.GenericAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    filterset_class = UnixDateFilter
    filter_backends = (DjangoFilterBackend,)

    def validate_urls(self, data):
        invalid_urls = []
        valid_urls = []
        for url in data:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                invalid_urls.append(url)
            else:
                valid_urls.append(url)
        return valid_urls, invalid_urls

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            distinct_names = queryset.values_list('name', flat=True).distinct()
            return Response({'domains': list(distinct_names), 'status': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get('links')
            if not data or not isinstance(data, list):
                return Response({'status': 'error', 'message': 'No links provided'}, status.HTTP_400_BAD_REQUEST)
            valid_urls, invalid_urls = self.validate_urls(data)

            domains = []
            for url in valid_urls:
                domain = urlparse(url).netloc
                domains.append({'name': domain})
            serializer = self.serializer_class(data=domains, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if invalid_urls:
                return Response(
                    {'status': 'warning', 'message': 'Some URLs were invalid', 'invalid_urls': invalid_urls},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
