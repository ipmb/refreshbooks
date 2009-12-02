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

def AuthorizingClient(domain, auth):
    """Creates a Freshbooks client for a freshbooks domain, using
    an auth object.
    """
    
    http_transport = transport.HttpTransport(api_url(domain), auth)
    
    return client.Client(
        adapters.xml_request,
        http_transport,
        functional.compose(
            adapters.fail_to_exception_response,
            objectify.fromstring
        )
    )

def TokenClient(domain, token):
    """Creates a Freshbooks client for a freshbooks domain, using
    token-based auth.
    """
    
    return AuthorizingClient(domain, transport.TokenAuthorization(token))

def OAuthClient(domain, consumer_key, consumer_secret, token, token_secret):
    """Creates a Freshbooks client for a freshbooks domain, using
    OAuth. Token management is assumed to have been handled out of band.
    """
    
    consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
    token = oauth.OAuthToken(token, token_secret)
    
    return AuthorizingClient(domain, transport.OAuthAuthorization(
        consumer,
        token
    ))

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