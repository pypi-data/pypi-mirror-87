import json
import urllib.request as urllib2
from distutils.version import StrictVersion


class PyPi(object):

    @classmethod
    def get_versions(self, package_name):
        url = "https://pypi.org/pypi/%s/json" % (package_name,)
        data = json.load(urllib2.urlopen(urllib2.Request(url)))
        versions = data["releases"].keys()
        versions = sorted(versions, key=StrictVersion)
        return versions

    @classmethod
    def get_current_version(self, package_name):
        return self.get_versions(package_name)[-1]

    @classmethod
    def get_latest_version(self, package_name):
        current = self.get_current_version(package_name).split(".")
        current[-1] = str(int(current[-1]) + 1)
        return ".".join(current)
