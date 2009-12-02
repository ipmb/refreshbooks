class RemoteMethod(object):
    """Ties python method calls into FreshBooks API calls.
    
    See Client.
    """
    
    def __init__(self, names, request_encoder, transport, response_decoder):
        self.names = names
        self.request_encoder = request_encoder
        self.transport = transport
        self.response_decoder = response_decoder
    
    def __call__(self, *args, **kwargs):
        method = '.'.join(self.names)
        
        request = self.request_encoder(method, *args, **kwargs)
        raw_response = self.transport(request)
        return self.response_decoder(raw_response)
    
    def __getattr__(self, name):
        return RemoteMethod(
            self.names + [name],
            self.request_encoder,
            self.transport,
            self.response_decoder
        )

class FailedRequest(Exception):
    def __init__(self, error):
        self.error = error
    
    def __str__(self):
        return repr(self.error)

class Client(object):
    """The Freshbooks API client. Callers should use one of the factory
    methods (BasicAuthClient, OAuthClient) to create instances.
    """
    
    def __init__(self, request_encoder, transport, response_decoder):
        self.request_encoder = request_encoder
        self.transport = transport
        self.response_decoder = response_decoder
    
    def __getattr__(self, name):
        return RemoteMethod(
            [name],
            self.request_encoder,
            self.transport,
            self.response_decoder
        )
