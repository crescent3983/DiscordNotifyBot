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

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--guild', type=str, help='guild name')
parser.add_argument('--channel', type=str, help='channel name')
parser.add_argument('--user', type=str, help='user name')
parser.add_argument('--message', type=str, help='text to send', required=True)

args = parser.parse_args()

if not (args.user or (args.guild and args.channel)):
    parser.error('-u/--user or -g/--guild and -c/--channel should specified')

# send text
url = "http://%s:%s/send_text" % (ip, port)

data = {}
if args.guild:
    data["guild"] = args.guild

if args.channel:
    data["channel"] = args.channel

if args.user:
    data["user"] = args.user

data["message"] = args.message

r = requests.post(url, json=data, auth=(user, password))
pretty_json = json.loads(r.text)
print (json.dumps(pretty_json, indent=2))
