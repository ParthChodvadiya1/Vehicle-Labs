from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

from rest_framework.pagination import LimitOffsetPagination
class StandardResultsSetPagination(LimitOffsetPagination, PageNumberPagination):
    default_limit = 5
    max_limit = 50
    page_size = 10
    page_size_query_param = 'page_size'
    offset_query_param = 'offset'
    limit_query_param = 'limit'
    
    max_page_size = 1000


class SmallPagesPagination(PageNumberPagination):  
    page_size = 5
    page_size_query_param = 'page_size'


class MyOffsetPagination(LimitOffsetPagination):
    
    offset_query_param = 'offset'
    page_size_query_param = 'page_size'