import os

from flask import Flask
from mandrill_webhooks import MandrillWebhooks

app = Flask(__name__)

if os.getenv('MANDRILL_WEBHOOKS_SETTINGS'):
    app.config.from_envvar('MANDRILL_WEBHOOKS_SETTINGS')

mandrill = MandrillWebhooks(app)


@mandrill.hook('*')
def log_event(payload, event):
    print "New event: %s received! with payload: %s" % (event, payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)