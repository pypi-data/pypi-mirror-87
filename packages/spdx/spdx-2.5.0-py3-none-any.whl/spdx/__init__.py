import copy
import json
import os.path
import sys

_IS_PY2 = sys.version_info[0] == 2
if _IS_PY2:
    import codecs
    open = codecs.open

_license_path = os.path.join(os.path.dirname(__file__), 'data')

with open(os.path.join(_license_path, 'db.json')) as f:
    db = json.load(f)
    _licenses = db['licenses']
    __version__ = db['version']
    del db

def _get_license(tmpl_name):
    path = os.path.join(_license_path, tmpl_name)
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError as e:
        with open(path, encoding='latin-1') as f:
            return f.read()

class License:
    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.__data)

    def __init__(self, record):
        self.__data = record
        self.__template = None
        self.__word_set = None

    @property
    def name(self):
        return self.__data['name']

    @property
    def id(self):
        return self.__data['id']

    @property
    def sources(self):
        return self.__data['sources']

    @property
    def notes(self):
        return self.__data['notes']

    @property
    def osi_approved(self):
        return self.__data['osi_approved']

    @property
    def header(self):
        return self.__data['header']

    @property
    def template(self):
        if self.__template is None:
            self.__template = _get_license(self.__data['template'])
        return self.__template

def licenses():
    return copy.deepcopy(_licenses)
