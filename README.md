```sh
$ cp parameters.dist.json parameters.json
```
Edit `parameters.json`

> You can obtain chat-id by starting chat with bot and requesting `https://api.telegram.org/bot#token#/getUpdates` method
```sh
$ python main.py # to exec one time
$ crontab -e # to plan the task
...
* * * * * python /path/to/rzd-parser/main.py
```