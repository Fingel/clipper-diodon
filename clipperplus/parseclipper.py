from HTMLParser import HTMLParser
import urllib2
from urllib import urlencode
import cookielib


class CSRFParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)
        self.ret = ''
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attr_d = dict(attrs)
            if attr_d['name'] == '_csrf_token':
                self.ret = attr_d['value']


class ClipsParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)
        self.ret = []
        self.recording = 0
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attrs:
            if name == 'href' and '/clippings/' in value:
                break
            else:
                return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'a' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.ret.append(data)


class ClipperParser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data = None

    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        # get CSRF token from homepage
        req = urllib2.urlopen("https://www.clippersync.com")
        csrf_parser = CSRFParser(req.read())
        csrf = csrf_parser.ret

        # do login post and store the page
        data = urlencode({'_csrf_token': csrf, 'email': self.username, 'password': self.password})
        req = urllib2.Request('https://www.clippersync.com/login', data)
        resp = urllib2.urlopen(req)
        self.data = resp.read()

    def show_data(self):
        print self.data

    def get_clippings(self):
        p = ClipsParser(self.data)
        return p.ret
