__all__ = ['getchangelog','gettimestamp']

from datetime import datetime, timedelta, timezone
import xmlrpc.client

class Change(list):
    @property
    def name(self):
        return self[0]

    @property
    def version(self):
        return self[1]

    @property
    def timestamp(self):
        return self[2]

    @property
    def action(self):
        return self[3]

def gettimestamp(value):
    if isinstance(value,datetime):
        return int(value.replace(tzinfo=timezone.utc).timestamp())
    if isinstance(value,(float,int)):
        return value
    if isinstance(value,timedelta):
        return int((datetime.now(timezone.utc)-value).timestamp())
    raise TypeError('unknown value %s' % value)

def getchangelog(timestamp,url=None):
    client = xmlrpc.client.ServerProxy(url if url else 'https://pypi.org/pypi')
    try:
        recentchanges = client.changelog(timestamp)
        return list(map(Change,recentchanges))
    except Exception:
        return []
