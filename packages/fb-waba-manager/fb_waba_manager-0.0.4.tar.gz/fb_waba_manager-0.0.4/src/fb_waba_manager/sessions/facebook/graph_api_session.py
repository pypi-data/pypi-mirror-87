from requests import Session
from ...constants.facebook.fb_constants import FbConstants
from ...constants.http.methods_constants import MethodsConstants

PAGING_KEY = 'paging'
NEXT_KEY = 'next'


class GraphApiSession:
    '''
    Provides a graph api requests session
    '''

    def __init__(self, access_token, version='v6.0'):
        self.access_token = access_token
        self.base_url = f'{FbConstants.GRAPH_API_BASE_URL}/{version}'
        self.session = Session()

    def build_url(self, node=None, edge=None, fields=[]):
        url = self.base_url
        if node is not None:
            url += f'/{node}'
        if edge is not None:
            url += f'/{edge}'
        if len(fields) > 0:
            url += f'?fields={",".join(fields)}&access_token={self.access_token}'
        else:
            url += f'?access_token={self.access_token}'
        return url

    def process_request(self, node=None, edge=None, fields=[], method=MethodsConstants.GET):
        url = self.build_url(node, edge, fields)
        response = None
        if method.upper() == MethodsConstants.GET:
            response = self.session.get(url)
        else:
            raise NotImplementedError(
                f'The method {method} is not implemented yet')

        try:
            return response.json()
        except Exception as ex:
            print(ex)
            return None

    def get_object(self, node=None, edge=None, fields=[]):
        return self.process_request(node, edge, fields, MethodsConstants.GET)

    def get_next_object(self, fb_response):
        try:
            return self.session.get(fb_response[PAGING_KEY][NEXT_KEY]).json()
        except Exception as ex:
            print(ex)
            return None
