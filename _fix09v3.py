# -*- coding: utf-8 -*-
import io, re

p = '09-buildreq.html'
s = io.open(p, encoding='utf-8').read()

def shiftnum(m):
    n = int(m.group(1))
    if 444 <= n <= 543:
        return '<span class="%s">%d</span>' % (m.group(2), n + 44)
    return m.group(0)

# 对 ln 与 ln-ref 内的数字做区间映射
s = re.sub(r'<span class="(ln|ln-ref)">(\d+)</span>', shiftnum, s)
s = re.sub(r'<span class="(ln|ln-ref)">(\d+)-(\d+)</span>',
           lambda m: '<span class="%s">%d-%d</span>' % (m.group(1), int(m.group(2)) + 44, int(m.group(3)) + 44)
           if 444 <= int(m.group(2)) <= 543 and 444 <= int(m.group(3)) <= 543 else m.group(0), s)

# 文本引用
R = [
    ('<code>agent.ts:444-543</code>', '<code>agent.ts:488-588</code>'),
    ('agent.ts:444 buildRequest', 'agent.ts:488 buildRequest'),
    ('<span class="ln-range">444-543</span>', '<span class="ln-range">488-588</span>'),
    ('看 554 行', '看 588 行'),
    ('这就是 460-464 行「effort 只在同模型时恢复」', '这就是 504-508 行「effort 只在同模型时恢复」'),
    ('llm/src/index.ts:890</code>', 'llm/src/index.ts:904</code>'),
    ('llm/src/index.ts:907-927', 'llm/src/index.ts:921-941'),
    ('llm/src/index.ts:904）', 'llm/src/index.ts:904）'),
    ('llm/src/index.ts:904</code>（10 页', 'llm/src/index.ts:904</code>（10 页'),
    ('在 895 行已 deepFreeze', '在 909 行已 deepFreeze'),
    ('（llm/src/index.ts:262，动态 adapter 可 override）', '（llm/src/index.ts:266，动态 adapter 可 override）'),
    ('session/src/types.ts:208）', 'session/src/types.ts:252）'),
    ('types.ts:290）', 'types.ts:293）'),
    ('（505-516 行）', '（549-563 行）'),
    ('（503-504 行）', '（549-550 行）'),
]
miss = 0
for a, b in R:
    n = s.count(a)
    if n == 0:
        miss += 1
        print('MISS:', a[:75])
    s = s.replace(a, b)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('09 done, misses =', miss)
