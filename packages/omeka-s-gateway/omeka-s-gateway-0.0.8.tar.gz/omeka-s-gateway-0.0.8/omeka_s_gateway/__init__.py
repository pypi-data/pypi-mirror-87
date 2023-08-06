import requests
import json
import pprint

class OmekaSGateway(object):
    def __init__(self, site_id, install_location, key_identity, key_credential):
        self.site_id = site_id
        self.install_location = install_location
        self.key_identity = key_identity
        self.key_credential = key_credential

    def set_site_id(self, site_id):
        self.site_id = site_id

    def get_request_info(self, endpoint):
        stock_parameters = {
            'site_id': self.site_id,
            'key_identity': self.key_identity,
            'key_credential': self.key_credential
        }
        uri = "{}/api/{}".format(self.install_location, endpoint)
        return (uri, stock_parameters)
        
    def create_page(self, data):
        uri, params = self.get_request_info('site_pages')
        r = requests.post(uri, params=params, json=data)
        return r.json()

    def get_page_by_slug(self, slug):
        return next((x for x in self.list_site_pages() if x['o:slug'] == slug), None)

    def get_item_by_title(self, title):
        return next((x for x in self.list_items() if x['o:title'] == title), None)

    def update_page(self, id_, data):
        uri, params = self.get_request_info('site_pages/' + id_)
        requests.put(uri, params=params, json=data)

    def list_site_pages(self):
        uri, params = self.get_request_info('site_pages')
        r = requests.get(uri, params=params)
        return r.json()

    def list_items(self):
        uri, params = self.get_request_info('items')
        r = requests.get(uri, params)
        return r.json()

    def list_vocabularies(self):
        uri, params = self.get_request_info('vocabularies')
        r = requests.get(uri, params)
        return r.json()

    def list_sites(self):
        uri, params = self.get_request_info('sites')
        r = requests.get(uri, params)
        return r.json()
    
    def create_item_with_media(self, item_payload, path, mime_type):
        uri, params = self.get_request_info('items')
        r = requests.post(uri, params=params, data={'data': json.dumps(item_payload)}, files=[
            ('file[0]', (path, open(path, 'rb'), mime_type))
        ])

        if r.ok:
            return r.json()
            print(r.status_code)
        else:
            raise Exception(r.json()['errors']['error'])



