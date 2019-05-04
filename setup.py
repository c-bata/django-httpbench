import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='djangohttpbench',
    version='0.1.0',
    packages=find_packages(),
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
