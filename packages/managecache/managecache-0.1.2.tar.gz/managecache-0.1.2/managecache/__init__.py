from pymemcache.client import base
import re, telnetlib, sys
client = base.Client(('localhost', 11211))

class MemcachedStats:

    _client = None
    _key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(r'STAT items:(.*):number')
    _stat_regex = re.compile(r"STAT (.*) (.*)\r")

    def __init__(self, host='localhost', port='11211', timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port,self._timeout)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write(("%s\n" % cmd).encode('ascii'))
        return self.client.read_until(b'END').decode('ascii')

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))
        
def get_connection_information():
    mem = MemcachedStats()
    for i,j in mem.stats().items():
        print(i," : " ,j)
def add_data():
    key=input("Enter key you want to add : ")
    result = client.get(key)
    if result:
        print("Already Exist :",key)
        print(result)
    if result is None:
        result = input("Enter value : ")
        client.set(key, result)
        print("Successfully Added")

def delete_data():
    key=input("Enter key you want to delete : ")
    result = client.get(key)
    if result:
        print("Deleting Key : ",key)
        client.delete(key)
        print("Successfully Deleted")
    if result is None:
        print("Key Not Found")

import os
def get_all_keys():
    print(os.system("memcdump --servers=localhost"))