import logging
import operator
import time
import threading

from datetime import datetime
from fractions import gcd
from urllib2 import urlopen, HTTPError, URLError
from yaml import safe_load


class PageStatusManager(object):
    """ PageStatusManager creates and runs/reports-on PageStatus. 
    """

    def __init__(self):
        self.ps = PageStatus()


    def run(self):
        elapsed = 0
        
        try:
            t = threading.Thread(target=self.ps.start, args=[])
            t.start()
        except:
            self.log.error("PageStatusManagerError: Could not create main run thread")
        
        while (t.isAlive()):
            time.sleep(self.ps.time_gcd)
            elapsed += self.ps.time_gcd
            
            if (elapsed % 60 == 0):
                longest_url = max(self.ps.url_response_time.iteritems(), key=operator.itemgetter(1))[0]
                http_codes = sorted(self.ps.http_count.items(), key=operator.itemgetter(1), reverse=True)[:5]
                self.ps.log.info(""" PageStatusManager Report ({} seconds)\n---------------------------------------------\
                \n- URL list: {}\
                \n- URL w/ longest response: {} ({} seconds)\
                \n- Top HTTP Codes (Code, Count): {}\
                \n- Num. URLs checked: {}\
                \n---------------------------------------------""".format(elapsed, self.ps.urls.keys(), longest_url, \
                                                                            self.ps.url_response_time[longest_url],
                                                                            http_codes, self.ps.url_check_count))
       
        t.join()
        

class PageStatus(object):
    """ PageStatus checks URL status as predefined intervals asynchronous.

    Attributes:
        url_fn (str): Name of JSON file containing URLs and intervals.
        log_fn (str): Name of URL status info log.
        max_duration (int): Duration of testing.
    """

    def __init__(self, url_fn="urls.json", log_fn="url_status.log", max_duration=300):
        self.urls = {}
        self.url_response_time = {}
        self.http_count = {}
        self.threads = []

        self.max_duration = max_duration
        self.url_check_count = 0 
        self.time_gcd = 1

        logging.basicConfig(filename=log_fn, level=logging.INFO)
        self.log = logging.getLogger()
        
        self.set_urls(url_fn)
        self.set_time_gcd()


    # To minimize some of the overhead
    # checks are made at GCD of all intervals
    def set_time_gcd(self):
        self.time_gcd = reduce(gcd, self.urls.values())


    def set_urls(self, fn):
        try:
            with open(fn) as f:
                data = safe_load(f)
        except IOError as e:
            print e

        for url_pair in data:
            self.urls[url_pair["url"]] = url_pair["interval"]


    def update_url_response_time(self, url, time):
        if self.url_response_time.get(url, 0) < time:
            self.url_response_time[url] = time


    def update_http_count(self, http_code):
        count = self.http_count.get(http_code, 0)
        self.http_count[http_code] = count + 1


    def update_url_check_count(self):
        self.url_check_count += 1


    def url_status(self, url):
        self.update_url_check_count()
        try:
            start_time = time.time()
            response = urlopen(url)
        except HTTPError as e:
            self.log.error("HTTPError: {} (HTTP {}) - {}".format(datetime.now(), e.code, url))
            self.update_http_count(e.code)
            self.update_url_response_time(url, time.time() - start_time)
            return False
        except URLError as e:
            self.log.error("URLError: {} - {}".format(datetime.now(), url))
            return False
        else:
            self.log.info(" {} - {} - {} Bytes".format(datetime.now(), url, len(response.read())))
            self.update_http_count(200)
            self.update_url_response_time(url, time.time() - start_time)
            return True
        
        
    def thread_clean(self):
        self.threads = [t for t in self.threads if not t.isAlive()]


    def start(self):
        elapsed = 0
        print "\nTesting page status through URL list.\n- Test duration: {} seconds\n- Check-in intervals: {} seconds\n".format(self.max_duration, self.time_gcd)

        # Spawn url_status threads when a correct interval is encountered
        while (elapsed <= self.max_duration):
            print "Elapsed time: {} seconds".format(elapsed)
            for url, interval in self.urls.iteritems():
                if (elapsed % interval == 0):
                    try:
                        t = threading.Thread(target=self.url_status, args=[url])
                        t.start()
                    except:
                        self.log.error("PageStatusError: Could not create thread for {} at runtime {} seconds".format(url, elapsed))
                    else:
                        self.threads.append(t)
            
            time.sleep(self.time_gcd)
            elapsed += self.time_gcd

            self.thread_clean()
        
        for t in self.threads:
            t.join()
