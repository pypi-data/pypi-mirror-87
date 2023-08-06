# pylint: skip-file
import asyncio
import unittest

from fastapi.responses import JSONResponse
from unimatrix.ext.model import exc

from ..views import APIView


class ExceptionHandlingTestCase(unittest.TestCase):

    def setUp(self):
        self.view = APIView()
        self.exception = exc.CanonicalException(http_status_code=500)

    def test_canonical_exception_produces_json_response(self):
        self.assertIsInstance(
            asyncio.run(self.view.handle_exception(self.exception)),
            (JSONResponse,)
        )

    def test_canonical_exception_produces_500(self):
        self.assertEqual(
            asyncio.run(self.view.handle_exception(self.exception)).status_code,
            500
        )
