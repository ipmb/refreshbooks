Refreshbooks provides a simple synchronous API for manipulating FreshBooks 
invoices, clients, and other data::

    from refreshbooks import api
    
    c = api.OAuthClient(
        'example.freshbooks.com',
        'consumerkey',
        'My Consumer Secret',
        'An existing token',
        'An existing token secret',
        user_agent='Example/1.0'
    )
    
    response = c.invoice.create(
        invoice=dict(
            client_id='8',
            lines=[
                api.types.line(
                    name='Yard Work',
                    unit_cost='10',
                    quantity='4'
                )
            ]
        )
    )
    
    invoice_response = c.invoice.get(
        invoice_id=response.invoice_id
    )
    
    print "New invoice created: #%s (id %s)" % (
        invoice_response.invoice.number,
        invoice_response.invoice.invoice_id
    )
    
    invoices_response = c.invoice.list()
    
    print "There are %s pages of invoices." % (
        invoices_response.invoices.attrib['pages'],
    )
    
    for invoice in invoices_response.invoices.invoice:
        print "Invoice %s total: %s" % (
            invoice.invoice_id,
            invoice.amount
        )

Consumer keys and secrets can be obtained from FreshBooks. This library
does not handle negotiating for an OAuth token+secret pair; see the
`oauth` module or the OAuth specification for details.

This library also supports the older token-based API authorization 
scheme::

    c = api.TokenClient(
        'example.freshbooks.com',
        'My API token',
        user_agent='Example/1.0'
    )
    
    # ... as above ...

API methods return lxml.objectify.ObjectifiedDataElement trees, which
can be manipulated as Python objects with the same structure as the 
underlying XML.

References:

 - http://developers.freshbooks.com/ - The FreshBooks API
 - http://developers.freshbooks.com/api/oauth/ - FreshBooks and OAuth