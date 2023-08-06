from ....factories.facebook.graph_api_factory import GraphApiFactory
from ....constants.facebook.fb_constants import FbConstants


PAGING_KEY = 'paging'
NEXT_KEY = 'next'
DATA_KEY = 'data'
ID_KEY = 'id'


class WabaService:

    def __init__(self, access_token):
        self.session = GraphApiFactory(access_token).get_session()

    def has_to_paginate_response(self, fb_response):
        return PAGING_KEY in fb_response and NEXT_KEY in fb_response[PAGING_KEY]

    def generate_fb_response(self, node, edge, fields=[]):
        # We will get a batch of data and yield it while we have to
        fb_response = self.session.get_object(node, edge, fields)
        has_to_paginate = True
        while has_to_paginate:
            for data in fb_response[DATA_KEY]:
                yield data
            has_to_paginate = self.has_to_paginate_response(fb_response)
            if has_to_paginate:
                fb_response = self.session.get_next_object(fb_response)

    def list_wabas(self, business_id):
        return self.generate_fb_response(business_id, FbConstants.WABAS_EDGE)

    def list_phone_numbers(self, waba_id):
        return self.generate_fb_response(waba_id, FbConstants.PHONE_NUMBERS_EDGE, fields=FbConstants.WABAS_FIELDS)

    def list_business_phone_numbers(self, business_id, wabas=None):
        '''
        params:
        wabas - must be a list of dict with 'id' key
        '''
        # if wabas is passed we will not fetch from GraphApi
        if wabas is not None:
            for waba in wabas:
                for pn in self.list_phone_numbers(waba[ID_KEY]):
                    yield pn
        else:
            for waba in self.list_wabas(business_id):
                for pn in self.list_phone_numbers(waba[ID_KEY]):
                    yield pn

    def list_message_templates(self, waba_id):
        return self.generate_fb_response(waba_id, FbConstants.MESSAGE_TEMPLATES_EDGE)
