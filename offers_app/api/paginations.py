from rest_framework.pagination import PageNumberPagination

""" Custom pagination-class to set default and max page sizes. """
class CustomResultSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20