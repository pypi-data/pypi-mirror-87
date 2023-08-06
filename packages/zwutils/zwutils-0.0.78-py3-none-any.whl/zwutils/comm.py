import re
import sys
import time
import collections
from difflib import SequenceMatcher

def ismac():
    return True if sys.platform == 'darwin' else False

def iswin():
    return True if sys.platform == 'win32' else False

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dict2attr(kv):
    kv = kv or {}
    o = type('', (), {})()
    for key, val in kv.items():
        setattr(o, key, val)
    return o

def attr2dict(o):
    o = o or type('', (), {})()
    r = {}
    attrs = [a for a in dir(o) if not a.startswith('_')]
    for attr in attrs:
        r[attr] = getattr(o, attr)
    return r

def tbl2dict(h, rs):
    '''h：表头list，rs：数据二维list。
    将每条数据（r）与表头按顺序匹配，形成dict list
    '''
    return [dict(zip(h, r)) for r in rs]

def extend_attrs(o, kv):
    o = o or type('', (), {})()
    kv = kv or {}
    if isinstance(o, dict):
        o = dict2attr(o)
    if not isinstance(kv, dict):
        kv = attr2dict(kv)

    for key, val in kv.items():
        setattr(o, key, val)
    return o

def upsert_config(cfg, cfg_val=None, def_val=None):
    """
    def_val's field will be ignored if field exists in cfg_val or cfg
    cfg_val's field will upsert into cfg no matter exists in cfg or not
    """
    def process_dict(rtn):
        attrs = dir(rtn)
        for attr in attrs:
            if attr.startswith('_'):
                continue
            attr_val = getattr(rtn, attr)
            if isinstance(attr_val, dict):
                setattr(rtn, attr, dict2attr(attr_val))
        return rtn
    if not cfg_val:
        return process_dict(extend_attrs(def_val, cfg))
    else:
        new_cfg = extend_attrs(def_val, cfg_val)
    return process_dict(extend_attrs(cfg, new_cfg))

def update_attrs(o, kv):
    o = o or type('', (), {})()
    kv = kv or {}
    if isinstance(o, dict):
        o = dict2attr(o)
    if not isinstance(kv, dict):
        kv = attr2dict(kv)

    for key, val in kv.items():
        if hasattr(o, key):
            setattr(o, key, val)
    return o

def print_duration(method):
    '''Prints out the runtime duration of a method in seconds
    usage:

    from zwutils.comm import print_duration

    @print_duration
    def test_func():
        pass

    test_func()
    '''
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%s cost %2.2f second(s)' % (method.__name__, te - ts))
        return result
    return timed

def list_intersection(a, b, ordered=False):
    if ordered:
        return [i for i, j in zip(a, b) if i == j]
    else:
        return list(set(a).intersection(b)) # choose smaller to a or b?

def list_split(arr, num):
    ''' split list into several parts
    '''
    rtn = []
    arrlen = len(arr)
    step = int(arrlen / num) + 1
    for i in range(0, arrlen, step):
        rtn.append(arr[i:i+step])
    return rtn

def list_uniqify(arr):
    '''Remove duplicates from provided list but maintain original order.
        Derived from http://www.peterbe.com/plog/uniqifiers-benchmark
    '''
    seen = {}
    result = []
    for item in arr:
        if item.lower() in seen:
            continue
        seen[item.lower()] = 1
        result.append(item.title())
    return result

def list_compare(a, b):
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    return compare(a, b)

def contains_digits(s):
    _digits = re.compile(r'\d')
    return bool(_digits.search(s))
