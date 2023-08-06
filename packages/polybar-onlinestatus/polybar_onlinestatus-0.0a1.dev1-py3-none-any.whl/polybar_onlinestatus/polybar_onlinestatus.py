

class OnlineStatus:
    """"""
    def __init__(self):
        self.url = "https://google.com"
        self.cache_timeout = 10
        self.timeout = 2
        self.offline_icon = ""
        self.online_icon = ""
        self.color = {
            "reset": "\u001b[0m",
            "offline": "\u001b[31m",
            "online": "\u001b[32m"
        }

    def check_online(self):
        from urllib.request import urlopen
        from urllib.error import URLError
        from subprocess import call
        if "://" in self.url:
            try:
                urlopen(self.url, timeout=self.timeout)
                return True
            except URLError:
                return False
        else:
            try:
                return call(['ping', '-c', '1', self.url]) == 0
            except URLError:
                return False

    @property
    def ping_url(self):
        return self.url

    @ping_url.setter
    def ping_url(self, new_url):
        self.url = new_url

    def online_result(self):
        if self.check_online():
            return f"{self.color['online']}{self.online_icon}{self.color['reset']}"
        else:
            return f"{self.color['offline']}{self.offline_icon}{self.color['reset']}"


