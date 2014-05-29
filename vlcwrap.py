#!  /usr/bin/python2
import urllib2
from urllib import quote
from lxml import etree

def parseplid(text):
    return text.split("_")[1]

def parseplaylist(playlist_xml):
    parsed = etree.fromstring(playlist_xml)
    for element in parsed[0]:
        vals = element.values()
        if len(vals) == 5:
            yield parseplid(vals[0]), vals[1]

# This module is the API layer between my server and VLC
# so it translates my requests into VLC requests that do the same thing...

# Adding a youtube video = adding the url to the playlist

class VLC(object):
    def __init__(self, servername, username, password):
        self.server = servername
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, self.server, username, password)
        handler = urllib2.HTTPBasicAuthHandler(passmgr)
        self.opener = urllib2.build_opener(handler)
        self.urlopen = self.opener.open

    def addFile(self, filename, encode=False):
        """
        Accepts URIs
        e.g. file://... http:// https://... and so on
        and makes a request to the VLC server
        """
        if encode:
            filename = quote(filename)
        response = self.urlopen("%s/requests/status.xml?command=in_enqueue&input=%s" % (self.server, filename))
        result = response.read()
        response.close()
        return result
    def shuffle(self):
        """
        Toggles shuffle on/off
        """
        response = self.urlopen("%s/requests/status.xml?command=pl_random" % self.server)
        result = response.read()
        response.close()
        return result
    def pause(self):
        """
        Toggles pause
        """
        response = self.urlopen("%s/requests/status.xml?command=pl_pause" % self.server)
        result = response.read()
        response.close()
        return result
    def next(self):
        """
        Moves to the next playlist item
        """
        response = self.urlopen("%s/requests/status.xml?command=pl_next" % self.server)
        result = response.read()
        response.close()
        return result
    def prev(self):
        """
        Moves to the previous playlist item
        """
        response = self.urlopen("%s/requests/status.xml?command=pl_previous" % self.server)
        result = response.read()
        response.close()
        return result
    def play(self, id_num):
        """
        play the specific playlist item
        """
        response = self.urlopen("%s/requests/status.xml?command=pl_play&id=%s" % (self.server, id_num))
        result = response.read()
        response.close()
        return result
    def vol(self, vol_level):
        """
        Set the volume to the given level
        """
        response = self.urlopen("%s/requests/status.xml?command=volume&val=%s" % (self.server, vol_level))
        result = response.read()
        response.close()
        return result
    def get_playlist(self):
        """
        Gets the entire playlist as an iterable of pairs of (playlist_id, filename)
        """
        response = self.urlopen("%s/requests/playlist_jstree.xml" % self.server)
        result = response.read()
        response.close()
        return parseplaylist(result)
    def __iter__(self):
        return self
