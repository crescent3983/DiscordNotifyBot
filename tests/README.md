# Examples

[中文版說明](./README_tc.md)

# Requirement

Python 3.7+

# Configuration(config.ini)

```ini
[WEB]
IP: IP
PORT: Port
USER: User
PASSWORD: Password
```

Should be the same as discord notify bot

# Test

## Get Channels

```bash
python get_channels.py 
```

## Get Memebers

```bash
python get_members.py 
```

## Send Text

```bash
python send_text.py \
    --user "804285680658284565" \
    --message "Hello World"
```

## Send Embed Message

```bash
python send_embed.py \
    --user "804285680658284565" \
    --title "Title" \
    --description "Description" \
    --color "0x3CD10C" \
    --fields "Line1" "Content1" "False" \
    --fields "Line2" "Content2" "True" \
    --fields "Line3" "Content3"
```