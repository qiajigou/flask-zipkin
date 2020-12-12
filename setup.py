import os

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_zipkin.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='Flask-Zipkin',
    version=__version__,
    url='https://github.com/qiajigou/flask-zipkin',
    license='BSD',
    author='killpanda',
    author_email='angus@killpanda.de',
    description='An zipkin extension for Flask based on py_zipkin.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['flask_zipkin'],
    zip_safe=False,
    platforms='any',
    test_suite='test_flask_zipkin',
    install_requires=[
        'Flask',
        'py_zipkin>=0.13.0',
        'requests>=2.11.1',
        ]
)
