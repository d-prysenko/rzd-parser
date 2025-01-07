# First start

Install dependencies
```sh
$ make deps
```
Make app config
```sh
$ make parameters.json
```
Edit `parameters.json`

> You can obtain chat-id by starting chat with bot and requesting `https://api.telegram.org/bot#token#/getUpdates` method
```sh
$ python main.py # to exec one time
$ crontab -e # to plan the task
...
* * * * * python /path/to/rzd-parser/main.py
```

# Filters
Filters placed in `filters/OfferFilters.py` and `filters/TrainFilters.py`, docs in `filters/FILTERS.md`.  
To update the filter doc use:
```sh
$ make docs
```