```sh
$ cp parameters.dist.json parameters.json
```
Edit `parameters.json`
```sh
$ python main.py -i # to init db before start
$ crontab -e
...
* * * * * python /path/to/Avito-Parser/main.py
```