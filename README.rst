Mandrill Webhooks
=================

|Flattr this repo|

Simple Flask extension to register functions to a mandrill hook


.. code-block:: python

    from flask import Flask
    from mandrill_webhooks import MandrillWebhooks
    
    app = Flask(__name__)
    mandrill = MandrillWebhooks(app)
    
    @mandrill.hook('open')
    def open_event(payload):
        """This code will be raised when open."""
        print "Open event received!"
    
    
    @mandrill.hook('*')
    def wildcard(payload, event):
        """This code will be raised for every event."""
        print "Event %s received!" % event
    
    
    # You can have more than one function for the same event
    
    @mandrill.hook('open')
    def another_open_event(payload):
        """This is another event code."""
        pass

.. |Flattr this repo| image:: http://api.flattr.com/button/flattr-badge-large.png
   :target: https://flattr.com/submit/auto?user_id=ecarreras&url=https://github.com/ecarreras/mandrill_webhooks&title=mandrill_webhooks&language=Python&tags=github&category=software
