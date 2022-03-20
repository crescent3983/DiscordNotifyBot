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

parser.add_argument('--title', type=str, help='title', required=True)
parser.add_argument('--description', type=str, help='description', required=True)
parser.add_argument('--color', type=str, help='hex color')
parser.add_argument('--fields', action='append', nargs='+', help='fields', required=True)

args = parser.parse_args()

if not (args.user or (args.guild and args.channel)):
    parser.error('-u/--user or -g/--guild and -c/--channel should specified')

# send embed
url = "http://%s:%s/send_embed" % (ip, port)

data = {}
if args.guild:
    data["guild"] = args.guild

if args.channel:
    data["channel"] = args.channel

if args.user:
    data["user"] = args.user

message = {}
data["message"] = message
message["title"] = args.title
message["description"] = args.description
if args.color:
    message["color"] = args.color

message["fields"] = []
for field in args.fields:
    if len(field) >= 2:
        name = field[0]
        value = field[1]
        inline = bool(field[2]) if len(field) >= 3 else False
        message["fields"].append({"name": name, "value": value, "inline": inline})

r = requests.post(url, json=data, auth=(user, password))
pretty_json = json.loads(r.text)
print (json.dumps(pretty_json, indent=2))
