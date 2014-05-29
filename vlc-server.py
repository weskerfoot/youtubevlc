import cherrypy
import vlcwrap
from urllib import unquote

class VLCServer(object):
    def __init__(self, remote_server, username, password):
        self.request = vlcwrap.VLC(remote_server, username, password)
        self.playlist = False
        self.top_id = 0

    def index(self):
        return ""

    def addyoutube(self, url, play):
        url = unquote(url)
        self.request.addFile(url, encode=True)
        if play == "true":
            self.playlatest()
        return str(self.top_id)

    def shuffle(self):
        return self.request.shuffle()

    def pause(self):
        return self.request.pause()

    def next(self):
        return next(self.request)

    def prev(self):
        return self.request.prev()

    def play(self, num_id):
        return self.request.play(num_id)

    def vol(self, vol_level):
        return self.request.vol(vol_level)

    def load_playlist(self):
        self.playlist = dict(self.request.get_playlist())
        return True

    def set_top_id(self):
        self.load_playlist()
        self.top_id = max((int(pid) for (pid, _) in self.playlist.items()))

    def playlatest(self):
        self.set_top_id()
        self.play(self.top_id)
        return str(self.top_id)

    index.exposed = True
    addyoutube.exposed = True
    shuffle.exposed = True
    pause.exposed = True
    next.exposed = True
    prev.exposed = True
    play.exposed = True
    vol.exposed = True
    playlatest.exposed = True

cherrypy.quickstart(VLCServer("http://192.168.2.10:8080", "username", "password")) # replace the example address
