# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def index_view(request):
    return Response('Hello world!')


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
