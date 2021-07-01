from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    max_limit = settings.MAX_PAGE_SIZE
