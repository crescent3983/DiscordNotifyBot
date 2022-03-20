import json, argparse, requests, os

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

DIR = os.path.dirname(os.path.realpath(__file__))

# config parser
config = configparser.ConfigParser()
config.read(DIR + "/config.ini")

ip = config.get("WEB", "IP")
port = config.get("WEB", "PORT")
user = config.get("WEB", "USER")
password = config.get("WEB", "PASSWORD")

# get channels
url = "http://%s:%s/get_channels" % (ip, port)

r = requests.get(url, auth=(user, password))
pretty_json = json.loads(r.text)
print (json.dumps(pretty_json, indent=2))
