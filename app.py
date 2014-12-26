import os

from flask import Flask
from mandrill_webhooks import MandrillWebhooks


from osconf import config_from_environment

app = Flask(__name__)


for k, v in config_from_environment('MANDRILL_WEBHOOKS').items():
    app.config['MANDRILL_WEBHOOKS_%s' % k.upper()] = v

mandrill = MandrillWebhooks(app)


@mandrill.hook('*')
def log_event(payload, event):
    print "New event: %s received! with payload: %s" % (event, payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)