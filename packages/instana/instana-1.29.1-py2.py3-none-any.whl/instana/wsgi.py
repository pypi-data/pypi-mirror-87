from __future__ import absolute_import

from .instrumentation.wsgi import InstanaWSGIMiddleware

# Alias for historical name
iWSGIMiddleware = InstanaWSGIMiddleware
