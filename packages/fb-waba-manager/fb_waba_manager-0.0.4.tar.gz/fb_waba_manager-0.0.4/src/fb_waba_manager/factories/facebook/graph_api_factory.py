from ...sessions.facebook.graph_api_session import GraphApiSession


class GraphApiFactory:
    '''
    Provides a graph api session
    '''

    def __init__(self, access_token):
        self.access_token = access_token
        self.session = GraphApiSession(access_token)

    def get_session(self):
        return self.session
