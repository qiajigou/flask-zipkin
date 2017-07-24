from __future__ import with_statement

# import sys
import unittest
import mock

import flask
from flask_zipkin import Zipkin


def handle_transport(*kargs, **kwargs):
    return True


class FlaskZipkinTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        app.testing = True
        app.config['ZIPKIN_DISABLE'] = False
        app.config['ZIPKIN_DSN'] = 'whatever'

        bp = flask.Blueprint('bp', __name__, url_prefix='/bp')

        @app.route('/foo')
        def foo():
            return 'bar'

        @bp.route('/bar')
        def bar():
            return 'foo'

        z = Zipkin()
        z._transport_handler = handle_transport

        self.z = z
        self.app = app
        self.app.register_blueprint(bp)
        z.init_app(self.app)

    @mock.patch('py_zipkin.zipkin.create_endpoint')
    def test_normal_get(self, create_endpoint_mock):
        rv = self.app.test_client().get('/foo')
        assert rv.status_code == 200

    @mock.patch('py_zipkin.zipkin.create_endpoint')
    def test_flask_request_context_with_app(self, create_endpoint_mock):
        with self.app.test_request_context('/foo'):
            self.app.preprocess_request()
            assert flask.g._zipkin_span
            assert flask.g._zipkin_span.span_name == 'foo.GET'

    @mock.patch('py_zipkin.zipkin.create_endpoint')
    def test_flask_request_context_with_bp(self, create_endpoint_mock):
        with self.app.test_request_context('/bp/bar'):
            self.app.preprocess_request()
            assert flask.g._zipkin_span
            assert flask.g._zipkin_span.span_name == 'bp.bar.GET'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlaskZipkinTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
