"""Setup script for django-massadmin"""
from setuptools import setup
from setuptools import find_packages


setup(
    name='django-massadmin',
    version='0.1',
    packages=find_packages(exclude=['test', 'tests',
                                    'example', 'demo']),
    include_package_data=True,
    license='BSD License',
    description='Make bulk changes in the Django admin interface',
    long_description=open('README').read(),
    author='Djaz Team',
    author_email='devweb@liberation.fr',
    url='http://www.liberation.fr/',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ])
