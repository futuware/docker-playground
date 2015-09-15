# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def index_view(request):
    dom_parts = request.domain.split('.')
    if len(dom_parts) == 2:
        subdomain = None
    elif len(dom_parts) == 3:
        subdomain = dom_parts[0]
    else:
        raise Exception
    return Response('Hello from {}'.format('base domain' if subdomain is None else subdomain))


def make_app():
    config = Configurator()
    config.add_view(index_view, route_name='index')
    config.add_route('index', '/')
    app = config.make_wsgi_app()
    return app


def main():
    app = make_app()
    server = make_server('0.0.0.0', 8080, app)
    print "Serving at :8080"
    server.serve_forever()


if __name__ == '__main__':
    main()
