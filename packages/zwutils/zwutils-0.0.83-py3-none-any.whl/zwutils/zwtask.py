import os
import sys
import time
import threading
import socket
import psutil
import requests
import logging
from multiprocessing import Process
from pathlib import Path

from zwutils.logger import add_filehandler
from zwutils.dlso import upsert_config
from zwutils.sysutils import iswin

class ZWTask(Process):
    STOP = 'stop'
    RUN = 'run'

    def __init__(self, target=None, name=None, args=None, daemon=True, checkfunc=None, cfg=None, **kwargs):
        super().__init__(name=name, daemon=daemon)
        cfgdef = {
            'c2server': 'http://localhost:13667/api/spider/status',
            'report_sleep': 30,
            'report_request_timeout': 3,
        }
        
        self.cfg = upsert_config(None, cfgdef, cfg, kwargs)
        self.hostname = socket.gethostname()
        self.target = target
        self.checkfunc = checkfunc

        _args = args or ()
        self.args = [self]
        self.args.extend(list(_args))

    def status_check(self):
        cfg = self.cfg
        while True:
            try:
                payload = {
                    'hname': self.hostname,
                    'pid': self.pid,
                    'pname': self.name,
                }
                if self.checkfunc:
                    o = self.checkfunc(self)
                    for p in o:
                        payload[p] = o[p]
                try:
                    r = requests.post(url=cfg.c2server, json=payload, timeout=cfg.report_request_timeout)
                    if r.status_code == 200:
                        r = r.json()
                        self.log(logging.INFO, 'code: %s'%r['code'])
                        if r['code'] == 1:
                            exit(0)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                time.sleep(cfg.report_sleep)
            except Exception as ex:
                pass

    def run(self):
        if self.target:
            thread_worker = threading.Thread(target=self.target, args=self.args, daemon=True)
            thread_checker = threading.Thread(target=self.status_check, daemon=True)
            thread_worker.start()
            thread_checker.start()
            thread_worker.join()
        self.log(logging.INFO, 'return.')
        exit(0)

    def suspend(self):
        self.log(logging.INFO, 'suspend.')
        if self.is_finish():
            return
        if not psutil.pid_exists(self.pid):
            return
        _psobj = psutil.Process(self.pid)
        _psobj.suspend()
    
    def resume(self):
        self.log(logging.INFO, 'resume.')
        if self.is_finish():
            return
        if not psutil.pid_exists(self.pid):
            return
        _psobj = psutil.Process(self.pid)
        _psobj.resume()
    
    def status(self):
        _psobj = psutil.Process(self.pid)
        if self.is_finish():
            return psutil.STATUS_STOPPED
        if not psutil.pid_exists(self.pid):
            return psutil.STATUS_STOPPED
        return _psobj.status()
    
    def is_finish(self):
        return self.exitcode == 0
    
    def log(self, lvl, msg):
        logmsg = '[%s] %s'%(self.pid, msg)
        logger = logging.getLogger(self.name)
        if not logger.hasHandlers():
            add_filehandler(filename='./logs/%s.log'%self.name)
        logger = logging.getLogger(self.name)
        logger.log(lvl, logmsg)

    @classmethod
    def run_processes(cls, target=None, name_prefix=None, args_list=None, max_size=5, timeslice=5, cfg=None, **kwargs):
        name_prefix = name_prefix or 'zwtask'
        args_list = args_list or []
        if not target:
            return

        running = []
        waiting = []
        for i,args in enumerate(args_list):
            if isinstance(args, dict):
                pname = args['pname']
                args = args['pargs']
            else:
                pname = '%s-%d' % (name_prefix, i)
            proc = ZWTask(target=target, name=pname, args=args, cfg=cfg, **kwargs)
            proc.start()
            proc.suspend()
            waiting.append(proc)

        while True:
            for i in range(len(running)-1, -1, -1):
                p = running[i]
                p.suspend()
                if p.is_finish():
                    p.terminate()
                else:
                    waiting.append(p)
                running.pop()

            arr = waiting[:max_size] if len(waiting)>max_size else waiting
            for p in arr:
                running.append(p)
                waiting.pop(0)
                p.resume()
            if len(running)==0 and len(waiting)==0:
                break
            time.sleep(timeslice)
    
    @classmethod
    def stop_processes(cls):
        pypth = os.path.abspath(sys.executable)
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            pyexe = proc.info['exe']
            if pyexe and 'python' in pyexe and pypth == proc.info['cmdline'][0]:
                procs.append(proc)
        infos = [{
            'pid': p.info['pid'],
            'cmd': p.info['cmdline'][0]
        } for p in procs]
        for proc in procs:
            p = psutil.Process(proc.info['pid'])
            p.kill()
        return pypth, infos