from lxml import etree

from refreshbooks import adapters

def test_request_xml_simple():
    xml = adapters.xml_request('client.list')
    
    # test that xml looks roughly like <request method="client.list"/>
    request_document = etree.fromstring(xml)
    assert 'request' == request_document.tag
    assert {'method': 'client.list'} == request_document.attrib
    assert 0 == len(request_document)

def test_request_xml_simple_params():
    xml = adapters.xml_request('client.get', id="5", monkey="butter")
    
    # test that xml looks roughly like either
    # <request method="client.get"><id>5</id><monkey>butter</monkey></request>
    # or
    # <request method="client.get"><monkey>butter</monkey><id>5</id></request>
    #
    # (We don't actually care which.)
    request_document = etree.fromstring(xml)
    assert 'request' == request_document.tag
    assert {'method': 'client.get'} == request_document.attrib
    assert 2 == len(request_document)
    assert any(
        parameter.tag == 'id' and parameter.text == '5'
        for parameter in request_document
    )
    assert any(
        parameter.tag == 'monkey' and parameter.text == 'butter'
        for parameter in request_document
    )

def test_request_xml_dict_params():
    xml = adapters.xml_request(
        'client.get',
        id="5",
        monkey=dict(name="butter")
    )
    
    # test that xml looks roughly like either
    # <request method="client.get">
    #     <id>5</id>
    #     <monkey><name>butter</name></monkey>
    # </request>
    # or
    # <request method="client.get">
    #     <id>5</id>
    #     <monkey><name>butter</name></monkey>
    # </request>
    #
    # (We don't actually care which.)
    request_document = etree.fromstring(xml)
    assert 'request' == request_document.tag
    assert {'method': 'client.get'} == request_document.attrib
    assert 2 == len(request_document)
    assert any(
        parameter.tag == 'id' and parameter.text == '5'
        for parameter in request_document
    )
    assert any(
        parameter.tag == 'monkey' 
        and len(parameter) == 1
        and parameter[0].tag == 'name'
        and parameter[0].text == 'butter'
        for parameter in request_document
    )

def test_request_xml_list_params():
    xml = adapters.xml_request(
        'client.get',
        id="5",
        monkeys=[
            ('monkey', dict(name="butter"))
        ]
    )
    
    # test that xml looks roughly like either
    # <request method="client.get">
    #     <id>5</id>
    #     <monkeys>
    #         <monkey><name>butter</name></monkey>
    #     </monkeys>
    # </request>
    # or
    # <request method="client.get">
    #     <monkeys>
    #         <monkey><name>butter</name></monkey>
    #     </monkeys>
    #     <id>5</id>
    # </request>
    #
    # (We don't actually care which.)
    request_document = etree.fromstring(xml)
    assert 'request' == request_document.tag
    assert {'method': 'client.get'} == request_document.attrib
    assert 2 == len(request_document)
    assert any(
        parameter.tag == 'id' and parameter.text == '5'
        for parameter in request_document
    )
    assert any(
        parameter.tag == 'monkeys' 
        and len(parameter) == 1
        and parameter[0].tag == 'monkey'
        and len(parameter[0]) == 1
        and parameter[0][0].tag == 'name'
        and parameter[0][0].text == 'butter'
        for parameter in request_document
    )
