name = 'nevermined-authlib'
version = '0.1.0'
author = 'Hsiaoming Yang <me@lepture.com>'
homepage = 'https://authlib.org/'
default_user_agent = '{}/{} (+{})'.format(name, version, homepage)

default_json_headers = [
    ('Content-Type', 'application/json'),
    ('Cache-Control', 'no-store'),
    ('Pragma', 'no-cache'),
]
