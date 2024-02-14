"""
ポリオミノの形から，マスごとの期待値を出す
↓
正方形で占う
↓
占いの結果/期待値の和、を期待値にかける
その上で、期待値高い順に掘る
↓
全ての油田を探し終えた時点で探索をやめる
"""
from collections import Counter
import sys
import copy

### 使用関数
def extract_squares_coordinates_grouped(N, d):
    squares = []
    for i in range(0, N, d):
        for j in range(0, N, d):
            # 一辺dの正方形または余白にある長方形のすべての座標を含むリストを作成
            square = []
            for di in range(min(d, N - i)):
                for dj in range(min(d, N - j)):
                    square.append((i + di, j + dj))
            squares.append(square)
    return squares

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

### 変更部分
# ある正方形について占う→その期待値を修正，を繰り返す
# 正方形のリストを生成
d = 3
coordinates_grouped = extract_squares_coordinates_grouped(N, d) # 占いに渡す座標のリストを生成

# 事後分布格納用リスト
coordinate_exp_fortune = copy.deepcopy(coordinate_exp)


for g in coordinates_grouped:
    # その正方形の期待値を取り出す
    ## その行の期待値の和を計算
    exp_sum_idx = 0
    for num in g:
        exp_sum_idx += coordinate_exp[num]
    ## 占い，倍率計算，修正
    ### 期待値0の場合は占わない
    if exp_sum_idx > 0:
        print("q {} {}".format(len(g), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), g))))
        resp = float(input()) # V(s)の近似値を受け取る
        num_times = resp / exp_sum_idx
        ## 期待値にかけ直す
        for num in g:
            val_raw = coordinate_exp[num]
            coordinate_exp_fortune[num] = val_raw * num_times
    else:
        pass


#print(coordinate_exp, file=sys.stderr)
#print(coordinate_exp_idx_col, file=sys.stderr)


# 一旦シンプルに，行占いで補正した期待値順に占って，掘り終わるまでやる
# 掘る順番
dig_order = dict(sorted(coordinate_exp_fortune.items(), key=lambda item: item[1], reverse=True)).keys()

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