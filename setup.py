import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-httpbench',
    version='0.0.1',
    packages=['httpbench'],
    description='HTTP load testing tools for Django. Like an apache bench '
                'but requests are sent from authenticated users.',
    long_description=README,
    author='Masashi Shibata',
    author_email='contact@c-bata.link',
    url='https://github.com/c-bata/django-httpbench',
    license='MIT',
    install_requires=[
        'Django',
        'requests',
    ]
)
