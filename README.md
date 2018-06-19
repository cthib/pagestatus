# Async. URL Status Checking
As part of a 6 hour project, designed and implemeted a system to report on URL statuses from predefined JSON list.   

### Setup:
1. Set up your virtualenv (Python 2.7): `mkvirtualenv pagestatus`
2. Get dependencies: `pip install -r requirements.txt`

### Main system
To use the system, use `python run.py`. The URLs and corresponding time intervals will be pulled from _urls.json_. The log entries will appear in _url_status.log_.

The URL checker is separated into two classes, `PageStatusManager` and `PageStatus`. The `PageStatusManager` is the main entry point that spawns a thread for one `PageStatus` and continues to report on it every 60 seconds. Once the `PageStatus` is initialized and started, it will use the given list of URL/interval pairs to create new url_status threads at the correct times. 

#### Extra info:
- To attempt to reduce overhead of the system, it becomes inactive for the greatest common denominator of all URL intervals.
- The current design doesn't deal with scalibility very well, but could be improved. By changing the PageStatus.urls dict to group the URLs with interval keys such as `{100: ["https://google.ca", "https://youtube.com"]}`. It seems more likely to have duplicate intervals rather than URLs. 

### Test cases
To run tests, change to the _pagestatus/_ dir and use `python pagestatus_test.py`.


