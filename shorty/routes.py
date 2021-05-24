from werkzeug.routing import Map
from werkzeug.routing import Rule
# Rule("/", endpoint="new_url"),
routes = Map([
    Rule("/static/<file>", endpoint="static", build_only=True),
    Rule("/", endpoint="/", build_only=True)
])