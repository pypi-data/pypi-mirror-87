from abc import ABCMeta


class APIEndpoint(metaclass=ABCMeta):
    def __init__(self, api, route, qs_args_def, body_args_def, business_class, authentication_required=True,
                 authorization_object=None, req_token='access'):
        pass
