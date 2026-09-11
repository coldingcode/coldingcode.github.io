# -*- coding: utf-8 -*-
"""Verify HTML line anchors against real source in D:/dev/sourcecode/deepseek-harness."""
import io, os, re, glob, sys, html as htmllib

REPO = 'D:/dev/sourcecode/deepseek-harness'

def strip_tags(fragment):
    text = re.sub(r'<[^>]+>', '', fragment)
    return htmllib.unescape(text)

def tokens(text):
    return set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', text))

# cache file lines
cache = {}
def lines_of(path):
    if path not in cache:
        full = os.path.join(REPO, path)
        if not os.path.isfile(full):
            cache[path] = None
        else:
            cache[path] = io.open(full, encoding='utf-8', errors='replace').read().split('\n')
    return cache[path]

results = []
for fn in sorted(glob.glob('*.html')):
    s = io.open(fn, encoding='utf-8').read()
    for fig in re.finditer(r'<figcaption>(.*?)</figcaption>(.*?)</code></pre>', s, re.S):
        cap, body = fig.group(1), fig.group(2)
        m = re.search(r'class="fname">([^<]+)</span>', cap)
        if not m:
            continue
        path = htmllib.unescape(m.group(1)).strip()
        if not path.endswith(('.ts', '.yml', '.yaml', '.json', '.md')):
            continue
        L = lines_of(path)
        if L is None:
            results.append((fn, path, 0, 'FILE-MISSING', ''))
            continue
        for cl in re.finditer(r'<span class="code-line[^"]*"><span class="ln">(\d+)</span>(.*?)</span>\s*(?:<span class="note">.*?</span>)?</span>', body, re.S):
            ln = int(cl.group(1))
            code = strip_tags(cl.group(2)).strip()
            if ln < 1 or ln > len(L):
                results.append((fn, path, ln, 'OUT-OF-RANGE', code[:60]))
                continue
            real = L[ln - 1]
            # HTML 片段可能把多条源码行折叠进一个 code-line：只比对首行
            code = code.split('\n')[0]
            # 文档常给源码加中文尾注（以 // 引出），与源码无关，比对前截掉
            code_ascii = code.split('//')[0] if not code.lstrip().startswith('//') else code
            want = tokens(code_ascii)
            # 去掉纯注释行噪音：只比较实质 token
            want = {t for t in want if len(t) > 1}
            if not want:
                continue
            have = tokens(real)
            hit = len(want & have) / len(want)
            # 折叠签名：HTML 把多行签名压成一行，此时真实首行是 HTML 文本的前缀
            if real.strip() and code.lstrip().startswith(real.strip()):
                continue
            if hit < 0.6:
                results.append((fn, path, ln, 'MISMATCH %.0f%%' % (hit * 100), code[:70] + '  ||REAL||  ' + real.strip()[:70]))

bad = [r for r in results if r[3] != 'FILE-MISSING' or True]
for fn, path, ln, kind, detail in bad:
    print('%-22s %-52s %5s  %-14s %s' % (fn, path, ln, kind, detail))
print('\nTOTAL issues:', len(bad))
