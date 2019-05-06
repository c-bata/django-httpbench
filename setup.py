import os
from setuptools import setup, find_packages

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(BASE_PATH, 'README.rst')) as f:
    README = f.read()

setup(
    name='djangohttpbench',
    version='0.1.0',
    packages=find_packages(),
    description='HTTP load testing tools for Django. Like an apache bench '
                'but requests are sent from authenticated users.',
    long_description=README,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ),
    keywords='django http benchmark',
    author='Masashi Shibata',
    author_email='contact@c-bata.link',
    url='https://github.com/c-bata/django-httpbench',
    license='MIT',
    install_requires=[
        'Django',
        'requests',
    ]
)
