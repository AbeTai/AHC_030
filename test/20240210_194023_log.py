"""
任意の大きさの正方形ずつ占う（あまりは長方形で対処）
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
# 各行→各列で行い，両方0のマス目は後回しで探索

fortune_res_idx = {}
idx_fortune_over0 = []
idx_fortune_0 = []

for f in range(N):
    # 占いに渡すリストを生成→横一行渡す
    fortune_input = []
    fortune_input = [(f, x) for x in range(N)]
    print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
    resp = float(input()) # V(s)の近似値を受け取る
    fortune_res_idx[f] = resp # key：行，val：その行のV(s)の近似値
    if resp > 0:
        idx_fortune_over0.append(f)
    else:
        idx_fortune_0.append(f)
        
fortune_res_col = {}
col_fortune_over0 = []
col_fortune_0 = []

for f in range(N):
    # 占いに渡すリストを生成→縦一列渡す
    fortune_input = []
    fortune_input = [(x, f) for x in range(N)]
    print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
    resp = float(input()) # V(s)の近似値を受け取る
    fortune_res_col[f] = resp # key：列，val：その列のV(s)の近似値
    if resp > 0:
        col_fortune_over0.append(f)
    else:
        col_fortune_0.append(f)

#print(fortune_res_idx, file=sys.stderr)
#print(fortune_res_col, file=sys.stderr)

# 両方0だったマスは探索範囲から消す
# TODO:片方でも0だったマスは探索範囲から消す

matching_cells = [(row, col) for row in range(N) for col in range(N) if fortune_res_idx[row] >= 1.0 and fortune_res_col[col] >= 1.0]
not_matching_cells = [(row, col) for row in range(N) for col in range(N) if fortune_res_idx[row] == 0.0 or fortune_res_col[col] == 0.0]
# print(matching_cells, file=sys.stderr)




# 占いの結果，行列が両方0より大きかったマスを探索
has_oil = []
oil_reserves = 0
for i,j in matching_cells:
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

#print("fortune miss", file=sys.stderr)
for i,j in not_matching_cells:
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