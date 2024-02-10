"""
占いを使ってみる
↓
全ての油田を探し終えた時点で探索をやめるよう変更する
"""

### ベース部分

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


### 占い部分

# 任意のマスずつ占いを使ってみる
# 今回は，簡単のため1行ずつやる

fortune_res = {}
idx_fortune_over0 = []
idx_fortune_0 = []

for f in range(N):
    # 占いに渡すリストを生成→横一行渡す
    fortune_input = []
    fortune_input = [(f, x) for x in range(N)]
    print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
    resp = float(input()) # V(s)の近似値を受け取る
    fortune_res[f] = resp # key：行，val：その行のV(s)の近似値
    if resp > 0:
        idx_fortune_over0.append(f)
    else:
        idx_fortune_0.append(f)

# print(fortune_res,idx_fortune_over0,idx_fortune_0, file=sys.stderr)


# 占いの結果，0より大きかった行から探索
has_oil = []
oil_reserves = 0
for i in idx_fortune_over0:
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

# print("fortune miss")
for i in idx_fortune_0:
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