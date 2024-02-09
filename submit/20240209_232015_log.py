"""
全ての油田を探し終えた時点で探索をやめるよう変更する
"""

import sys

# read prior information
line = input().split()
N = int(line[0])
M = int(line[1])
eps = float(line[2])
fields = []
for _ in range(M):
    line = input().split()
    ps = []
    for i in range(int(line[0])):
        ps.append((int(line[2*i+1]), int(line[2*i+2])))
    fields.append(ps)

# 油田のマス目のユニーク数(重複削除)
tmp = []
for m in range(M):
    tmp.extend(fields[m])
oil_grid_unique = len(set(tmp))

# drill every square
has_oil = []
for i in range(N):
    for j in range(N):
        print("q 1 {} {}".format(i, j))
        resp = input()
        #print(resp,type(resp), file=sys.stderr)
        if resp != "0":
            has_oil.append((i, j))
            print(len(has_oil), file=sys.stderr)

        if len(has_oil) == oil_grid_unique:
            print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))),  file=sys.stderr)
            resp = input()
            print(resp, file=sys.stderr)
            assert resp == "1"