# microbot 🎤 🤖

![image](https://user-images.githubusercontent.com/46664545/116843996-bc32bb80-abaf-11eb-8d7a-95d01616ffaa.png)

```bash
# Install
curl https://raw.githubusercontent.com/minelminel/microbot/master/install.sh | bash

# Run
gunicorn \
  'microbot.core:create_app()' \
  --name=microbot \
  --workers=1 \
  --worker-connections 1000 \
  --bind=localhost:5000 \
  -k gevent
```

```bash
# Daemon
sudo apt-get install -y nginx
sudo cp ./system/microbot.{service,socket} /etc/systemd/system/
sudo cp ./system/microbot.conf /etc/nginx/conf.d/
sudo systemctl enable --now nginx.service
sudo systemctl daemon-reload
```


### TODO:
- settings page which allows runtime adjustment of properties such as delay, step mode, min/max, etc
- calibration workflow and code, including test cases


Websocket Message - Data Model

```js

{
    // what is the purpose of the message?
    // ex. "info" | "error" | "message"
    type: str,
    // epoch milliseconds
    // ex. 1619829580766
    time: int,
    // corresponds to the topic
    // ex. "axis.motion"
    room: str,
    // description & context
    // ex. "x-axis slider update"
    memo: str,
    // arbitrary payload
    // ex. { "X": 10 } | "A"
    data: any
    // random unique identifier
    // ex. "fa80d178-b87b-4360-ad90-83ca0888d41d"
    guid: str
}
```
