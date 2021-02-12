import requests
import json
import time
import sys
import select
import const as const
from datetime import datetime
from random import randrange

fp = open(const.requestLog, 'a')


def takeInput():
    print('within ' + str(const.TIMEOUT) +
          ' r/R to retry or w/W to wait or any other key to continue')
    i, _, _ = select.select([sys.stdin], [], [], const.TIMEOUT)
    if (i):
        return sys.stdin.readline().strip()
    else:
        return


def apiCall(url):
    #time.sleep(randrange(10))
    fp.write(url+'\n')
    while 1:
        try:
            reply = requests.get(url)
            reply = reply.json()

        except Exception as e:
            print("caught Exception "+str(e))

            print('will try after ' + str(const.TIMEOUT)+' seconds')
            time.sleep(const.TIMEOUT)
            continue

        if 'error' in reply:
            if reply['error']['code'] == 17 or reply['error']['code'] == 4 or reply['error']['code'] == 32:
                print("request limit reached")
                print("cur Time "+str(datetime.now()))
                print("will wait for "+str(const.WAIT)+" seconds")
                time.sleep(const.WAIT)
            elif reply['error']['code'] == 190:
                print('Token Expired')
                sys.exit()
            else:
                print('Error=====================>')
                print(reply['error'])
                print()

                s = takeInput()
                if s == 'R' or s == 'r':
                    continue
                if s == 'W' or s == 'w':
                    print('will try after ' + str(const.TIMEOUT)+' seconds')
                    time.sleep(const.TIMEOUT)
                    continue
                else:
                    return reply

        else:
            print('*')
            return reply
