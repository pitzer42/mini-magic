from flask import abort, request
from functools import wraps


def inject_json_fields(*fields):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if request.json is None:
                abort(400, description='json was expected in the request')
            for field in fields:
                if field not in request.json:
                    abort(400, description=field + ' field was expected in json request')
                kwargs[field] = request.json[field]
            return view(*args, **kwargs)
        return wrapped_view
    return decorator


def get_or_404(func, *args):
    doc = func(*args)
    if doc is None:
        abort(404)
    return doc
