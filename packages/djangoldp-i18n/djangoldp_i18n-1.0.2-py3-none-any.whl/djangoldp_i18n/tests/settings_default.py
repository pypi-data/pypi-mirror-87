
from djangoldp.tests.settings_default import *

DJANGOLDP_PACKAGES=['djangoldp.tests', 'djangoldp_i18n.tests']
INSTALLED_APPS=('django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'modeltranslation',
                'django.contrib.admin',
                'django.contrib.messages',
                'guardian',
                'djangoldp',
                'djangoldp.tests',
                'djangoldp_i18n.tests')

AUTH_USER_MODEL='tests.User'

USE_I18N = True

LANGUAGES = [
    ('en', 'English'),
    ('en-gb', 'English GB'),
    ('en-us', 'English US'),
    ('fr', 'Français'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': (),
    'en-gb': ('en','en-us',),
    'en-us': ('en', 'en-gb',),
    'en': ('en-gb', 'en-us')
}

LDP_RDF_CONTEXT={
   "@vocab": "http://happy-dev.fr/owl/#",
   "foaf": "http://xmlns.com/foaf/0.1/",
   "doap": "http://usefulinc.com/ns/doap#",
   "ldp": "http://www.w3.org/ns/ldp#",
   "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
   "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
   "xsd": "http://www.w3.org/2001/XMLSchema#",
   "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
   "acl": "http://www.w3.org/ns/auth/acl#",
   "name": "rdfs:label",
   "website": "foaf:homepage",
   "deadline": "xsd:dateTime",
   "lat": "geo:lat",
   "lng": "geo:long",
   "jabberID": "foaf:jabberID",
   "permissions": "acl:accessControl",
   "mode": "acl:mode",
   "view": "acl:Read",
   "change": "acl:Write",
   "add": "acl:Append",
   "delete": "acl:Delete",
   "control": "acl:Control"
}
