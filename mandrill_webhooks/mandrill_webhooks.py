# -*- coding: utf- 8 -*-
from __future__ import absolute_import
from base64 import b64encode
import hmac
from hashlib import sha1
import json

from blinker import signal
from flask import request
from werkzeug.exceptions import BadRequest


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

    @staticmethod
    def raise_signal():
        if request.method == 'HEAD':
            return 'To be or not to be...', 200
        mandrill_events = request.form.get('mandrill_events')
        if not mandrill_events:
            raise BadRequest('No valid payload detected')

    @staticmethod
    def hook(event):
        def _wrapper(fn):
            event_signal = signal(event)
            event_signal.connect(fn)
            return fn
        return _wrapper