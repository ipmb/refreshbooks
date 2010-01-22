import sys
import functools

import functional
from lxml import objectify
import oauth.oauth as oauth

from refreshbooks import client, adapters, transport

def api_url(domain):
    """Returns the Freshbooks API URL for a given domain.
    
        >>> api_url('billing.freshbooks.com')
        'https://billing.freshbooks.com/api/2.1/xml-in'
    """
    return "https://%s/api/2.1/xml-in" % (domain, )

default_request_encoder = adapters.xml_request
default_response_decoder = functional.compose(
    adapters.fail_to_exception_response,
    objectify.fromstring
)

def logging_request_encoder(method, **params):
    encoded = default_request_encoder(method, **params)
    
    print sys.stderr, "--- Request (%r, %r) ---" % (method, params)
    print encoded
    
    return encoded

def logging_response_decoder(response):
    print sys.stderr, "--- Response ---"
    print response
    
    return default_response_decoder(response)

def AuthorizingClient(domain, auth, request_encoder, response_decoder):
    """Creates a Freshbooks client for a freshbooks domain, using
    an auth object.
    """
    
    http_transport = transport.HttpTransport(
        api_url(domain),
        transport.KeepAliveHeaders(auth)
    )
    
    return client.Client(
        request_encoder,
        http_transport,
        response_decoder
    )

def TokenClient(
    domain,
    token,
    request_encoder=default_request_encoder,
    response_decoder=default_response_decoder
):
    """Creates a Freshbooks client for a freshbooks domain, using
    token-based auth.
    
    The optional request_encoder and response_decoder parameters can be
    passed the logging_request_encoder and logging_response_decoder objects
    from this module, or custom encoders, to aid debugging or change the
    behaviour of refreshbooks' request-to-XML-to-response mapping.
    """
    
    return AuthorizingClient(
        domain,
        transport.TokenAuthorization(token),
        request_encoder,
        response_decoder
    )

def OAuthClient(
    domain,
    consumer_key,
    consumer_secret,
    token,
    token_secret,
    request_encoder=default_request_encoder,
    response_decoder=default_response_decoder
):
    """Creates a Freshbooks client for a freshbooks domain, using
    OAuth. Token management is assumed to have been handled out of band.
    
    The optional request_encoder and response_decoder parameters can be
    passed the logging_request_encoder and logging_response_decoder objects
    from this module, or custom encoders, to aid debugging or change the
    behaviour of refreshbooks' request-to-XML-to-response mapping.
    """
    
    consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
    token = oauth.OAuthToken(token, token_secret)
    
    return AuthorizingClient(
        domain,
        transport.OAuthAuthorization(
            consumer,
            token
        ),
        request_encoder,
        response_decoder
    )

def list_element_type(_name, **kwargs):
    """Convenience function for creating tuples that satisfy
    adapters.encode_as_list_of_dicts().
    
        >>> list_element_type('foo', a='5')
        ('foo', {'a': '5'})
    """
    return _name, kwargs

class Types(object):
    """Convenience factory for list elements in API requests.
    
        >>> types = Types()
        >>> types.line(id="5")
        ('line', {'id': '5'})
    
    A module-scoped instance is available as refreshbooks.api.types.
    """
    
    def __getattr__(self, name):
        return functools.partial(list_element_type, name)

types = Types()