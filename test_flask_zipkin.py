from __future__ import with_statement

# import sys
import unittest
import mock

from flask import Flask
from flask_zipkin import Zipkin


def handle_transport(*kargs, **kwargs):
    return True


class FlaskZipkinTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.testing = True
        app.config['ZIPKIN_DISABLE'] = False
        app.config['ZIPKIN_DSN'] = 'whatever'

        z = Zipkin()
        z.init_app(app)
        z._transport_handler = handle_transport

        self.z = z
        self.app = app

        @app.route('/foo')
        def foo():
            return 'bar'

    @mock.patch('py_zipkin.zipkin.create_endpoint')
    def test_normal_get(self, create_endpoint_mock):
        rv = self.app.test_client().get('/foo')
        assert rv.status_code == 200


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlaskZipkinTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
