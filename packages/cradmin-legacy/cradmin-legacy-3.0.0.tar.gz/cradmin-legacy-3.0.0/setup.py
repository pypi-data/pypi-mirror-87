import json
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'cradmin_legacy', 'version.json')) as f:
    version = json.loads(f.read())

setup(
    name='cradmin-legacy',
    description='Legacy 1.x fork of django cradmin.',
    version=version,
    url='https://github.com/appressoas/cradmin_legacy',
    author='Espen Angell Kristiansen, Tor Johansen, Vegard Angell, Magne Westlie',
    author_email='post@appresso.no',
    license='BSD',
    packages=find_packages(
        exclude=[
            'ez_setup',
            'tasks'
        ]),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Django>=3.1.0,<4.0.0',
        'django-cradmin>=8.0.2,<9.0.0',
        'ievv-opensource>=7.0.3,<8.0.0',
        'django-multiupload',
        'Jinja2',
        'pytz',
        'future',
        'html2text'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
