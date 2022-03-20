# 測試範例

# 需求

Python 3.7+

# 設定檔(config.ini)

```ini
[WEB]
IP: 位址
PORT: 端口
USER: 使用者
PASSWORD: 密碼
```

填上與機器人服務端一樣的參數

# 測試

## 取得所有頻道

```bash
python get_channels.py 
```

## 取得所有成員

```bash
python get_members.py 
```

## 傳送一般訊息

```bash
python send_text.py \
    --user "804285680658284565" \
    --message "Hello World"
```

## 傳送embed訊息

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