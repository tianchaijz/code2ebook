#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import psutil
import multiprocessing
from subprocess import Popen

home_path = os.path.expanduser("~")
base_path = os.path.join(home_path, "code")
gen_file = os.path.join(home_path, "tools/code2ebook/gen.sh")
tmp_dir = os.path.join(home_path, "tmp/ebook")


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.get_children(recursive=True):
        proc.kill()
        process.kill()


def shell(command):
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    try:
        process = Popen(
            args=command,
            stdout=sys.stdout,
            shell=True,
            preexec_fn=os.setsid)
        return process.communicate()[0]
    except KeyboardInterrupt:
        print "\n==== " + repr(process)
        kill(process.pid)


def worker(info):
    if info['path'][0] == '$':
        path = os.path.expandvars(info['path'])
    else:
        path = os.path.join(base_path, info['path'])

    title = info.get('title', info['path'].split('/')[-1])
    pdf_name = "%s.pdf" % title.replace('-', '_')

    with cd(path):
        shell("%s %s %s" % (gen_file, title, pdf_name))


def dummy_worker(info):
    title = info.get('title', info['path'].split('/')[-1])
    pdf_name = "%s.pdf" % title.replace('-', '_')

    with cd(tmp_dir):
        shell('output=$(ls -l | grep {0}); if [ -z "$output" ]; then echo {0}; \
              fi'.format(pdf_name))

jobs = [
    {'path': "interesting/CaoE"},
    {'path': "interesting/tcviz"},
    {'path': "interesting/canything"},
    {'path': "interesting/recipes", 'title': "chenshuo-recipes"},
    {'path': "c/interactive-c-demo", 'title': "interactive-c"},
    {'path': "c/busybox/coreutils", 'title': "busybox-coreutils"},
    {'path': "c/coreutils/src", 'title': "coreutils"},
    {'path': "c/linenoise"},
    {'path': "c/hiredis"},
    {'path': "socket/socket-server"},
    {'path': "socket/ssocks-0.0.14/src", 'title': "ssocks"},
    {'path': "socket/kcp"},
    {'path': "socket/shadowsocks-libev/src", 'title': "shadowsocks-libev"},
    {'path': "socket/shadowsocks"},
    {'path': "socket/ssocks5"},
    {'path': "socket/mongoose"},
    {'path': "socket/uhttpd"},
    {'path': "socket/weighttp/src", 'title': "weighttp"},
    {'path': "socket/wrk"},
    {'path': "socket/muduo"},
    {'path': "socket/memcached"},
    {'path': "socket/sniproxy", 'title': "sni_proxy"},
    {'path': "test/libev/libev-examples"},
    {'path': "c_plus_plus/vczh_toys", 'title': "vczh-toys"},
    {'path': "adt/lstack"},
    {'path': "task/ltask"},
    {'path': "task/simplethread"},
    {'path': "task/coroutine"},
    {'path': "reading/Source/tinyhttpd"},
    {'path': "lang/shine"},
    {'path': "lang/mini"},
    {'path': "lang/luna"},
    {'path': "lang/lua"},
    {'path': "lang/streem"},
    {'path': "lang/luajit-lang-toolkit"},
    {'path': "lib/twisted"},
    {'path': "lib/multiprocessing"},
    {'path': "lib/scapy"},
    {'path': "lib/requests"},
    {'path': "spider/pyspider"},
]


_jobs = [
    {'path': "lang/cpython"},
    {'path': "lang/lua"},
    {'path': "cpp/leveldb"},
]

_jobs = [
    {'path': "$HOME/openresty/lua-nginx-module/src",
     'title': "lua-nginx-module"},
    {'path': "$HOME/source/_code/luna", 'title': "airtrack-luna"},
    {'path': "$HOME/source/_code/memcached", 'title': "memcached"},
    {'path': "$HOME/source/_code/leveldb", 'title': "leveldb"},
    {'path': "$HOME/source/_code/mread", 'title': "mread"},
]

_jobs = [
    {'path': "$HOME/source/_code/tinypie/src/tinypie", 'title': "tinypie"},
]


def main():
    pool = multiprocessing.Pool(processes=8)

    run = True

    if run:
        try:
            pool.map_async(worker, _jobs)
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            print "==== Main terminate!"
            kill(os.getpid())
    else:
        pool.map(dummy_worker, _jobs)
        pool.close()
        pool.join()

    print "Total %d items converted!" % len(jobs)
    shell("ls -l ~/tmp/ebook | grep rw | wc -l")


if __name__ == '__main__':
    shell("mkdir -p " + tmp_dir)
    main()
