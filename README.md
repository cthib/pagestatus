# Async. URL Status Checking
As part of a 6 hour project, designed and implemeted a system to report on URL statuses from predefined JSON list.

### Project Requirements
- Need to check a list of urls at regular intervals, to make sure these are reachable and that we can get their content. The program will be fed from a JSON file with a list of predefined urls and check intervals. 
- As output, provide **timestamp**,  **url** and **length of the body**. 
- Need to respect _as much as possible_ the defined schedule. This means you have to think of a solution that isn't affected by the time a single URL takes, nor by the fact that some URLs fail. Consider the best design pattern for this.
- Error handling in case a URL returns a code different than `200` (consider some URLs migh be permanently unreachable but some other might just have a temporary glitch..)
- Data on the status of the system should be logged every minute (Num. URLs checked, Top 5 HTTP codes, URLs currently being checked, URL that has taken the longest to respond)
- Consider that there might be a _huge_ list of urls, but the system has only limited resources (workers) for checking them 

### Setup:
1. Set up your virtualenv (Python 2.7): `mkvirtualenv pagestatus`
2. Get dependencies: `pip install -r requirements.txt`

### Main system
To use the system, use `python run.py`. The URLs and corresponding time intervals will be pulled from _urls.json_. The log entries will appear in _url_status.log_.

The URL checker is separated into two classes, `PageStatusManager` and `PageStatus`. The `PageStatusManager` is the main entry point that spawns a thread for one `PageStatus` and continues to report on it every 60 seconds. Once the `PageStatus` is initialized and started, it will use the given list of URL/interval pairs to create new url_status threads at the correct times. 

#### Lessons learned:
Spawning new threads is not the most memory efficient approach for I/O networking tasks. A better solution would be to use coroutines to check the status of the pages. I would like to improve upon this system by moving to Python3 and asyncio to allow for a higher _worker_ amount. 

### Test cases
To run tests, change to the _pagestatus/_ dir and use `python pagestatus_test.py`.


