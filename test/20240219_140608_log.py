"""
ポリオミノの形から，マスごとの期待値を出す
↓
正方形で占う
↓
占いの結果/期待値の和、を期待値にかける
※ここで，占いの結果が0だった場合，0.5をかけるように修正
その上で、期待値高い順に掘る
↓
占いのマスを細かくしてもう一回
さっきの結果と平均（算術or調和）or最大値をとる
↓
あるマスを掘った値に応じて隣接マスの事後確率を更新
※隣接マスの範囲を拡大
↓
これで終わらない場合，占いをミスった部分を最後に探索
↓
全ての油田を探し終えた時点で探索をやめる
"""
from collections import Counter
import sys
import copy
import numpy as np

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

def generate_neighboor_coordinates(i, j, N):
    adjacent_coordinates = []
    # Up
    if i > 0:
        adjacent_coordinates.append((i - 1, j))
    # Down
    if i < N - 1:
        adjacent_coordinates.append((i + 1, j))
    # Left
    if j > 0:
        adjacent_coordinates.append((i, j - 1))
    # Right
    if j < N - 1:
        adjacent_coordinates.append((i, j + 1))
    return adjacent_coordinates

def generate_neighboor_coordinates_cross(i, j, N):
    adjacent_coordinates = []
    # Up
    if i > 0 and j > 0:
        adjacent_coordinates.append((i - 1, j - 1))
    if i > 0 and j < N -1:
        adjacent_coordinates.append((i - 1, j + 1))
    if i < N - 1 and j > 0:
        adjacent_coordinates.append((i + 1, j - 1))
    if i < N - 1 and j < N - 1:
        adjacent_coordinates.append((i + 1, j + 1))
    return adjacent_coordinates

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
d = 8
d2 = 3
coordinates_grouped = extract_squares_coordinates_grouped(N, d) # 占いに渡す座標のリストを生成
coordinates_grouped_another = extract_squares_coordinates_grouped(N, d2) # 占いに渡す座標のリストを生成

# 事後分布格納用リスト
coordinate_exp_fortune = copy.deepcopy(coordinate_exp)
coordinate_exp_fortune_another = copy.deepcopy(coordinate_exp)

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
        if resp > 0:
            num_times = resp / exp_sum_idx
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune[num] = val_raw * num_times
        ##################### 修正部分 #########################
        else:
            num_times = resp / exp_sum_idx
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune[num] = val_raw * num_times

    else:
        pass

### 細かいマスでもう一回
for g in coordinates_grouped_another:
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
        if resp > 0:
            num_times = resp / exp_sum_idx
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune_another[num] = val_raw * num_times
        ##################### 修正部分 #########################
        else:
            if exp_sum_idx == 0:
                num_times = 0
            else:
                num_times = resp / exp_sum_idx
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune_another[num] = val_raw * num_times

    else:
        pass

for idx in coordinate_exp_fortune.keys():
    coordinate_exp_fortune[idx] = np.mean([coordinate_exp_fortune[idx], coordinate_exp_fortune_another[idx]])
    # coordinate_exp_fortune[idx] = np.sqrt(coordinate_exp_fortune[idx] * coordinate_exp_fortune_another[idx])
    # coordinate_exp_fortune[idx] = max(coordinate_exp_fortune[idx], coordinate_exp_fortune_another[idx])


# 外した時用に，元々期待値0で，占いで0になったマスのリスト作る
# 元々0のリスト
coordinate_exp_0 = [key for key, value in coordinate_exp.items() if value == 0]
# 占いで0のリスト
coordinate_exp_fortune_0 = [key for key, value in coordinate_exp_fortune.items() if value == 0]
# 差分
possible_miss_list = list(set(coordinate_exp_fortune_0) - set(coordinate_exp_0))
#print(coordinate_exp_0, file=sys.stderr)
#print(coordinate_exp_fortune_0, file=sys.stderr)
#print(possible_miss_list, file=sys.stderr)

# 占い後の事後確率高い順に修正
dig_order = list(dict(sorted(coordinate_exp_fortune.items(), key=lambda item: item[1], reverse=True)).keys())
#print(dig_order, file=sys.stderr)

has_oil = []
oil_reserves = 0

# ルールベースならグリッドサーチ
# アルゴリズムは考える
up_times = 1000
up_times_cross = 1.5
down_times = 0.4
down_times_cross = 0.2

for _ in range(N*N):
    #print(len(dig_order), file=sys.stderr)
    (i,j) = dig_order[0]
    #print((i,j), file=sys.stderr)
    #print(dig_order[0], file=sys.stderr)
    print("q 1 {} {}".format(i, j))
    resp = int(input())
    oil_reserves += resp
    #print(oil_reserves, file=sys.stderr)
    coordinate_exp_fortune[(i,j)] = 0
    coordinate_next = generate_neighboor_coordinates(i,j,N)
    coordinate_next_cross = generate_neighboor_coordinates_cross(i,j,N)

    # 変更部分
    ## 占いの結果によって事後確率を更新
    if resp > 0:
        has_oil.append((i,j))
        
        #print(coordinate_next, file=sys.stderr)
        #sys.exit()
        for n in coordinate_next:
            coordinate_exp_fortune[n] = up_times * coordinate_exp_fortune[n]
        
        for n in coordinate_next_cross:
            coordinate_exp_fortune[n] = up_times_cross * coordinate_exp_fortune[n]
        
        dig_order = list(dict(sorted(coordinate_exp_fortune.items(), key=lambda item: item[1], reverse=True)).keys())
        
        if oil_reserves == oil_grid_num:
            print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
            resp = input()
            # print(resp, file=sys.stderr)
            # assert resp == "1"
            sys.exit()

    else:
        for n in coordinate_next:
            coordinate_exp_fortune[n] = down_times * coordinate_exp_fortune[n]
        
        for n in coordinate_next_cross:
            coordinate_exp_fortune[n] = down_times_cross * coordinate_exp_fortune[n]
        
        dig_order = list(dict(sorted(coordinate_exp_fortune.items(), key=lambda item: item[1], reverse=True)).keys())
        
    if set(coordinate_exp_fortune.values()) == {0}:
        print("miss", file = sys.stderr)
        for (i,j) in possible_miss_list:
            print("q 1 {} {}".format(i, j))
            resp = int(input())
            oil_reserves += resp
            if resp > 0:
                has_oil.append((i,j))

            if oil_reserves == oil_grid_num:
                print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
                resp = input()
                # print(resp, file=sys.stderr)
                # assert resp == "1"
                sys.exit()

