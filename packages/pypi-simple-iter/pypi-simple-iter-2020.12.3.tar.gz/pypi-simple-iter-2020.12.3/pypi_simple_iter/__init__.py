__all__ = ['iter_projects_from_file']

import os
import tempfile
from tempfile import mkstemp, mkdtemp

import pypi_slug
import requests_retry_on_exceptions as requests


def iter_projects_from_file(path, startswith=None):
    with open(path) as f:
        for l in filter(lambda l: 'href' in l, f):
            name = l.split('>')[1].split('<')[0]
            slug = pypi_slug.getslug(name)
            if startswith and slug[0:len(startswith)] == pypi_slug.getslug(startswith):
                yield slug, name
            if not startswith:
                yield slug, name


def iter_projects(url=None, startswith=None):
    f, path = tempfile.mkstemp()
    os.close(f)
    try:
        r = requests.get(url if url else 'https://pypi.org/simple/')
        open(path, 'w').write(r.text)
        for slug, name in iter_projects_from_file(path, startswith=startswith):
            yield slug, name
    finally:
        os.unlink(path)
