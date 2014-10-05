# -*- coding: utf- 8 -*-
from __future__ import absolute_import
from base64 import b64encode
import hmac
from hashlib import sha1
import json

from blinker import signal
from flask import request
from werkzeug.exceptions import BadRequest


import sys

if sys.version < '3':
    def b(x):
        return x
else:
    import codecs

    def b(x):
        return codecs.latin_1_encode(x)[0]


class MandrillWebhooks(object):
    def __init__(self, app=None):
        """Init method.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.validate_signature)
        self.set_defaults()
        prefix = self.app.config['MANDRILL_WEBHOOKS_PREFIX']
        app.add_url_rule(prefix, 'raise_signal', self.raise_signal,
                         methods=['POST', 'HEAD'])

    def set_defaults(self):
        self.app.config.setdefault('MANDRILL_WEBHOOKS_PREFIX', '/mandrill')

    def validate_signature(self):
        if request.path != self.app.config['MANDRILL_WEBHOOKS_PREFIX']:
            return
        if request.method == 'HEAD':
            return
        #if not self.app.debug:
        if True:
            key = self.app.config.get('MANDRILL_WEBHOOKS_KEY')
            api_url = self.app.config.get('MANDRILL_WEBHOOKS_URL')
            signature = request.headers.get('X-Mandrill-Signature')
            if not signature:
                raise BadRequest('This missage is not signed')
            if key:
                payload = api_url
                post = request.form
                for key in sorted(post.keys()):
                    payload += '%s%s' % (key, post[key])
                digest = b64encode(hmac.new(b(key), b(payload), sha1))
                if digest != signature:
                    raise BadRequest('Wrong HMAC signature')

    @staticmethod
    def raise_signal():
        if request.method == 'HEAD':
            return 'To be or not to be...', 200
        mandrill_events = request.form.get('mandrill_events')
        if not mandrill_events:
            raise BadRequest('No valid payload detected')
        mandrill_events = json.loads(mandrill_events)
        for payload in mandrill_events:
            event = payload.get('event')
            if not event:
                # Mandrill webhooks are not unified for sync events
                event = payload.get('action')
            if not event:
                raise BadRequest('No event defined in payload')
            broadcast_signal = signal('*')
            if broadcast_signal.receivers:
                broadcast_signal.send(payload, event=event)
            event_signal = signal(event)
            if event_signal.receivers:
                event_signal.send(payload)
        return 'Hook delivered', 200

    @staticmethod
    def hook(event):
        def _wrapper(fn):
            event_signal = signal(event)
            event_signal.connect(fn)
            return fn
        return _wrapper