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


# 油田のマス目の数(重複あり)
tmp = []
for m in range(M):
    tmp.extend(fields[m])
oil_grid_num = len(tmp)


# drill every square
has_oil = []
oil_reserves = 0
for i in range(N):
    for j in range(N):
        print("q 1 {} {}".format(i, j))
        resp = int(input())
        oil_reserves += resp
        # print(resp,oil_reserves, file=sys.stderr)

        if resp > 0:
            has_oil.append((i, j))

        if oil_reserves == oil_grid_num:
            print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
            resp = input()
            # print(resp, file=sys.stderr)
            # assert resp == "1"
            sys.exit()

"""
        if resp > 0:
            has_oil.append((i, j))
            print(len(has_oil),oil_grid_num, file=sys.stderr)

        if len(has_oil) == oil_grid_num or len(has_oil) == N**2:
            # print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))),  file=sys.stderr)
            print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
            resp = input()
            print(resp, file=sys.stderr)
            # assert resp == "1"
            sys.exit()
"""