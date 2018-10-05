import sys

import urllib2
import math
import re
from bs4 import BeautifulSoup
from pprint import pprint
from threading import Thread
from collections import deque
from time import sleep
import timeit

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36"
SEARCH_URL = "https://google.com/search"
RESULT_SELECTOR = "h3.r a"
TOTAL_SELECTOR = "#resultStats"
RESULTS_PER_PAGE = 10
DEFAULT_HEADERS = [
        ('User-Agent', USER_AGENT),
        ("Accept-Language", "en-US,en;q=0.5"),
    ]
SCALE_FACTOR = 1.5
#SCALE_FACTOR = 1 # when monitor is connected

X0 = str(int(1360 * SCALE_FACTOR))
Y0 = str(int(284 * SCALE_FACTOR))
X1 = str(int(1690 * SCALE_FACTOR))
Y1 = str(int(640 * SCALE_FACTOR))

userin = ''
while userin != 'exit':
    start = timeit.default_timer()

    cmd = 'cd ../Capture2Text_v4.5.1_64bit & Capture2Text_CLI.exe -b --screen-rect \\\"' + X0 + ' ' + Y0 + ' ' + X1 + ' ' + Y1 + '\\\" '
    scan = !{cmd}
    print(scan)
    answers = []
    if len(scan) > 3 and len(scan) < 15:
        c = 0
        for a in reversed(scan):
            c += 1
            if a != '':
                answers.append(a)
                if len(answers) > 2:
                    break
        question = ' '.join(scan[0:(-1 * c)])
        #print(answers)
        #print(question)
        for a in reversed(answers):
            opener = urllib2.build_opener()
            opener.addheaders = DEFAULT_HEADERS
            query = question + "\\" + a + "\\"
            #print(query)
            response = opener.open(SEARCH_URL + "?q="+ urllib2.quote(query))
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            totalText = soup.select(TOTAL_SELECTOR)[0].children.next().encode('utf-8')
            total = long(re.sub("[', ]", "", re.search("(([0-9]+[', ])*[0-9]+)", totalText).group(1)))
            output = a + ": " + str(total)
            print(output)
    else:
        print("input too large; make sure OCR is working correctly")


    stop = timeit.default_timer()
    print stop - start

    userin = raw_input("type exit to exit")
