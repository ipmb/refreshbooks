from lxml import etree
from refreshbooks import elements

def test_field():
    field_element = elements.field("example", "A Test Value Here")
    
    assert "<example>A Test Value Here</example>" == etree.tostring(
        field_element
    )

def test_simple_type_strings():
    type_element = elements.type("example", [
        elements.field('name', 'Bob'),
        elements.field('age', '27')
    ])
    
    assert 'example' == type_element.tag
    assert 2 == len(type_element)
    assert 'name' == type_element[0].tag
    assert 'Bob' == type_element[0].text
    assert 'age' == type_element[1].tag
    assert '27' == type_element[1].text

def test_simple_request():
    body = elements.field("foo", "bar")
    
    request_element = elements.request("client.list", [body])
    
    assert 'request' == request_element.tag
    assert {'method': 'client.list'} == request_element.attrib
    assert 1 == len(request_element)
    assert body == request_element[0]
