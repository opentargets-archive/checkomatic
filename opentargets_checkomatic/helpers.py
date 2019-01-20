import os
import urllib
import addict
import opentargets as ot


def to_vlist(iterable):
    return [match.value for match in iterable]


def to_vset(iterable):
    return set(to_vlist(iterable))


def failed_at(s):
    print("failed at", s)


def make_client(host, port):
    return ot.OpenTargetsClient(host=host, port=port)


def make_local_env(*args, **kwargs):
    return addict.Dict(*args, **kwargs).to_dict()


def uri_open_and_read(uri):
    quoted_uri = urllib.quote(uri)
    if ('http://' not in quoted_uri) and ('https://' not in quoted_uri):
        if 'file://' not in quoted_uri:
            quoted_uri = 'file://' + urllib.quote(os.path.abspath(uri))

    return urllib.urlopen(quoted_uri).read()
