"""
ポリオミノの形から，マスごとの期待値を出す
↓
期待値高いところから占う
↓
掘る
↓
占う
↓
...
↓
全ての油田を探し終えた時点で探索をやめる
"""
from collections import Counter
import sys
### ベース部分
# read prior information
line = input().split()
N = int(line[0])
M = int(line[1])
eps = float(line[2])
fields = []
square_list = []
for _ in range(M):
    line = input().split()
    ps = []
    square_list.append(int(line[0]))
    for i in range(int(line[0])):
        ps.append((int(line[2*i+1]), int(line[2*i+2])))
    fields.append(ps)
#print(square_list, file=sys.stderr)
    
# 全マス目の一覧を生成
coordinate_pool = []
for i in range(N):
    for j in range(N):
        coordinate_pool.append((i,j))

# 油田のマス目の数(重複あり)
tmp = []
for m in range(M):
    tmp.extend(fields[m])
oil_grid_num = len(tmp)

### マスごとの期待値を計算（事前分布的なもの）
# 計算前(全て0)
coordinate_exp = dict(zip(coordinate_pool,[0]*len(coordinate_pool)))
# 各ポリオミノについて計算
for pol in fields:
    coordinate_exp_tmp = dict(zip(coordinate_pool,[0]*len(coordinate_pool)))
    # 並行移動可能幅を定義
    max_polyomino_x = max([x[0] for x in pol])
    max_polyomino_y = max([x[1] for x in pol])
    low_move = N - max_polyomino_x
    light_move = N - max_polyomino_y
    print(low_move,light_move, file=sys.stderr)

    for low in range(low_move):
        for light in range(light_move):
            coordinate_possible = [(x[0]+low, x[1]+light) for x in pol]
            # 要素の出現回数をカウント
            element_counts = Counter(coordinate_possible)
            # 既存の辞書に出現回数を足し算
            for key, count in element_counts.items():
                coordinate_exp_tmp[key] += count
    divider = low_move * light_move
    coordinate_exp_tmp_div = {key: value / divider for key, value in coordinate_exp_tmp.items()}

    # 既存の辞書に出現回数を足し算
    for key, count in coordinate_exp_tmp_div.items():
        coordinate_exp[key] += count

#print(coordinate_exp, file=sys.stderr)

# 一旦シンプルに，期待値順に占って，掘り終わるまでやる
# 掘る順番
dig_order= dict(sorted(coordinate_exp.items(), key=lambda item: item[1], reverse=True)).keys()

has_oil = []
oil_reserves = 0

for (i, j) in dig_order:
    print("q 1 {} {}".format(i, j))
    resp = int(input())
    oil_reserves += resp
    if resp > 0:
            has_oil.append((i, j))

    if oil_reserves == oil_grid_num:
        print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
        resp = input()
        # print(resp, file=sys.stderr)
        # assert resp == "1"
        sys.exit()