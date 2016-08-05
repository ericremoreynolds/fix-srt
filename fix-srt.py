import sys
import re

def read_time(t):
    if ',' in t:
        t, ms = t.split(',')
    else:
        ms = 0
    ms = int(ms)
    h, m, s = map(int, t.split(':'))
    return ms + 1000 * (s + 60 * (m + 60 * h))

def fmt_time(t):
    ms = t % 1000
    t //= 1000
    s = t % 60
    t //= 60
    m = t % 60
    t //= 60
    h = t
    return "{:02}:{:02}:{:02},{:03}".format(h, m, s, ms)

def read_sub(i, ls):
    idx = int(ls[i])
    i += 1
    times = map(read_time, ls[i].split(' --> '))
    i += 1
    text = []
    while i < len(ls) and ls[i].strip():
        text.append(ls[i].strip())
        i += 1
    return i+1, {
        'index': idx,
        'times': times,
        'text': text
    }

def read_srt(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    i = 0
    subs = []
    while i < len(lines):
        i, sub = read_sub(i, lines)
        subs.append(sub)
    return subs

def write_srt(subs, fn):
    with open(fn, 'w') as f:
        for sub in subs:
            f.write("%s\n%s --> %s\n%s\n\n" % (
                sub['index'],
                fmt_time(sub['times'][0]),
                fmt_time(sub['times'][1]),
                "\n".join(sub['text'])
            ))

fn = sys.argv[1]
fn_fixed = fn[:fn.rfind('.')] + ".fixed" + fn[fn.rfind('.'):]

subs = read_srt(fn)

if len(sys.argv) == 2:
    for sub in subs:
        t1, t2 = sub['times']
        idx = "{:6}".format(sub['index'])
        print(idx + "  " + fmt_time(t1) + "  " + " / ".join(sub['text']))
elif len(sys.argv) == 4:
    idx = int(sys.argv[2])
    t = read_time(sys.argv[3])
    sub, = (s for s in subs if s['index'] == idx)
    t0, _ = sub['times']
    shift = t - t0
    print("Shifting by %s ms, writing to '%s'" % (shift, fn_fixed))
    for sub in subs:
        t0, t1 = sub['times']
        sub['times'] = (t0 + shift, t1 + shift)
    write_srt(subs, fn_fixed)
elif len(sys.argv) == 6:
    idxA = int(sys.argv[2])
    tA = read_time(sys.argv[3])
    idxB = int(sys.argv[4])
    tB = read_time(sys.argv[5])
    subA, = (s for s in subs if s['index'] == idxA)
    subB, = (s for s in subs if s['index'] == idxB)
    t0A, _ = subA['times']
    t0B, _ = subB['times']
    def trans_time(t):
        w = float(t - t0A) / (t0B - t0A)
        return int((1 - w) * tA + w * tB)
    print("Writing to '%s'" % (fn_fixed))
    for sub in subs:
        sub['times'] = map(trans_time, sub['times'])
    write_srt(subs, fn_fixed)
else:
    print("Invalid args")
