import mock
from mock import sentinel

from refreshbooks import client

def test_arbitrary_method():
    request_encoder = mock.Mock()
    request_encoder.return_value = sentinel.request
    
    transport = mock.Mock()
    transport.return_value = sentinel.transport_response
    
    response_decoder = mock.Mock()
    response_decoder.return_value = sentinel.response
    
    test_client = client.Client(
        request_encoder,
        transport,
        response_decoder
    )
    
    response = test_client.arbitrary.method(id=5)
    
    assert (('arbitrary.method', ), dict(id=5)) == request_encoder.call_args
    assert ((sentinel.request, ), {}) == transport.call_args
    assert ((sentinel.transport_response, ), {}) == response_decoder.call_args
    assert sentinel.response == response
