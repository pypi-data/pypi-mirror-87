
import os

class OGCAPI(object):
    def __init__(self, config):
        self.config = config

        self.url = os.path.join(self.config.get('server', 'url'), 'oapir')

    def handle(self, headers, args):
        self.headers = headers
        self.args = args

        path = list(filter(None, headers['PATH_INFO'].split('/')))

        if len(path) == 1 and path[0] == 'oapir':
            r = self.landing_page()
        if len(path) == 2 and path[1] == 'conformance':
            r = self.conformance()

        return ('application/json', r)

    def landing_page(self):
        return {
            'title': self.config.get('metadata:main', 'identification_title'),
            'description': self.config.get('metadata:main', 'identification_abstract'),
            'links': [{
                'rel': 'self',
                'type': 'application/json',
                'title': 'This document as JSON',
                'href': os.path.join(self.url)
                }, {
                'rel': 'conformance',
                'type': 'application/json',
                'title': 'Conformance',
                'href': os.path.join(self.url, 'conformance')
                }, {
                'rel': 'data',
                'type': 'application/json',
                'title': 'Collections',
                'href': os.path.join(self.url, 'collections')
            }]
        }

    def conformance(self):
        return {    
            'conformsTo': [
                'http://www.opengis.net/spec/ogcapi-records-1/1.0/conf/core',
                'http://www.opengis.net/spec/ogcapi-records-1/1.0/conf/oas30',
                'http://www.opengis.net/spec/ogcapi-records-1/1.0/conf/geojson'
            ]
        }
