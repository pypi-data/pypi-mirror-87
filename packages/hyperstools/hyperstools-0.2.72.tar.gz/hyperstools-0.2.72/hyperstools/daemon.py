import os
import sys


def daemonize():
    """将程序变成守护进程"""
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    os.chdir(".")
    os.setsid()
    os.umask(0)
    _pid = os.fork()
    if _pid > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stdin.flush()
    sys.stderr.flush()
    si = open(str("stdin"), "a+")
    so = open(str("stdout"), "a+")
    se = open(str("stderr"), "a+")
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
