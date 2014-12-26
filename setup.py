from setuptools import setup

setup(
    name='mandrill_webhooks',
    version='0.1.0',
    packages=['mandrill_webhooks'],
    url='https://github.com/ecarreras/mandrill_webhooks',
    license='MIT',
    install_requires=['flask', 'blinker'],
    author='ecarreras',
    author_email='ecarreras@gmail.com',
    description='Flask Webhooks'
)
