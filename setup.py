from setuptools import setup

setup(
    name='Flask-Elasticsearch',
    version='1.0',
    url='https://github.com/CalthorpeAnalytics/flask-elasticsearch.git',
    author='bryanculbertson',
    author_email='bryan@urbanfootprint.com',
    description='Access to Elasticsearch in your Flask app.',
    py_modules=['flask_elasticsearch'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'elasticsearch>=7.0.0',
        'elasticsearch-dsl>=7.0.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
