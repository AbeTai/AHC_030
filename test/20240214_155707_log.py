"""
ポリオミノの形から，マスごとの期待値を出す
↓
クロスで占う
↓
占いの結果/期待値の和、を期待値にかける
その上で、期待値高い順に掘る
↓
全ての油田を探し終えた時点で探索をやめる
"""
from collections import Counter
import sys
import copy
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
    #print(low_move,light_move, file=sys.stderr)

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
coordinate_exp_idx = copy.deepcopy(coordinate_exp)
### 変更部分
# ある行について占う→その行の期待値を変更，を繰り返す
for idx in range(N):
    # 占い
    fortune_input = [(idx, x) for x in range(N)]
    print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
    resp = float(input()) # V(s)の近似値を受け取る
    """
    if idx == 14:
        print(resp, file = sys.stderr)
    """

    # その行の期待値を取り出す
    ## その行のマスを生成
    coordinate_idx_tmp = [(idx, col) for col in range(N)]
    ## その行の期待値の和を計算
    exp_sum_idx = 0
    for col in range(N):
        exp_sum_idx += coordinate_exp[coordinate_idx_tmp[col]]
    ## 倍率計算
    num_times = resp / exp_sum_idx
    ## 期待値にかけ直す
    for col in range(N):
        val_raw = coordinate_exp[coordinate_idx_tmp[col]]
        coordinate_exp_idx[coordinate_idx_tmp[col]] = val_raw * num_times

coordinate_exp_col = copy.deepcopy(coordinate_exp)
# ある列について占う→その列の期待値を変更，を繰り返す
for col in range(N):
    # 占い
    fortune_input = [(x, col) for x in range(N)]
    print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
    resp = float(input()) # V(s)の近似値を受け取る
    """
    if col == 13:
        print(resp, file = sys.stderr)
    """

    # その行の期待値を取り出す
    ## その行のマスを生成
    coordinate_col_tmp = [(x, col) for x in range(N)]
    ## その行の期待値の和を計算
    exp_sum_col = 0
    for idx in range(N):
        exp_sum_col += coordinate_exp[coordinate_col_tmp[idx]]
    ## 倍率計算
    num_times = resp / exp_sum_col
    ## 期待値にかけ直す
    for idx in range(N):
        val_raw = coordinate_exp[coordinate_col_tmp[idx]]
        coordinate_exp_col[coordinate_col_tmp[idx]] = val_raw * num_times

coordinate_exp_idx_col = copy.deepcopy(coordinate_exp)

# 行列占い後の結果をかける
for ic in coordinate_exp.keys():
    idx_val = coordinate_exp_idx[ic]
    col_val = coordinate_exp_col[ic]
    coordinate_exp_idx_col[ic] = idx_val * col_val

#print(coordinate_exp, file=sys.stderr)
#print(coordinate_exp_idx_col, file=sys.stderr)


# 一旦シンプルに，行占いで補正した期待値順に占って，掘り終わるまでやる
# 掘る順番
dig_order = dict(sorted(coordinate_exp_idx_col.items(), key=lambda item: item[1], reverse=True)).keys()

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