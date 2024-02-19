"""
ポリオミノの形から，マスごとの期待値を出す
↓
正方形で占う
↓
占いの結果/期待値の和、を期待値にかける
※ここで，占いの結果が0だった場合，0.5をかけるように修正
その上で、期待値高い順に掘る
↓
あるマスを掘った値に応じて，
1以上：そのマスが存在するパターンの期待値を上げる，存在しないパターンの期待値を下げる
0：存在するパターンの期待値を下げる，存在しないパターンの期待値を上げる
↓
これで終わらない場合，事前分布で期待値0じゃないけど掘ってない部分を最後に探索
↓
全ての油田を探し終えた時点で探索をやめる
"""
from collections import Counter
import sys
import copy
from turtle import down

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

# 各ポリオミノのありうるパターンを格納 [[(i,j)]]
# 今回はポリオミノごとを考慮した事後確率更新を行わないので，ポリオミノごとに座標をまとめる必要がない
# ポリオミノごとに事後確率更新の計算を別個に行う場合は，ネストをもう一つ深くする[[[(i,j)]]]
coordinate_possible_patern = []
# 各ポリオミノについて計算
for pol in fields:
    # coordinate_possible_patern_poly = []
    coordinate_exp_tmp = dict(zip(coordinate_pool,[0]*len(coordinate_pool)))
    # 並行移動可能幅を定義
    max_polyomino_x = max([x[0] for x in pol])
    max_polyomino_y = max([x[1] for x in pol])
    low_move = N - max_polyomino_x
    light_move = N - max_polyomino_y
    #print(low_move,light_move, file=sys.stderr)

    for low in range(low_move):
        for light in range(light_move):
            coordinate_possible_tmp = [(x[0]+low, x[1]+light) for x in pol]
            # ありうるパターンを追加
            coordinate_possible_patern.append(coordinate_possible_tmp)
            # 要素の出現回数をカウント
            element_counts = Counter(coordinate_possible_tmp)
            # 既存の辞書に出現回数を足し算
            for key, count in element_counts.items():
                coordinate_exp_tmp[key] += count
    divider = low_move * light_move
    coordinate_exp_tmp_div = {key: value / divider for key, value in coordinate_exp_tmp.items()}

    # 既存の辞書に出現回数を足し算
    for key, count in coordinate_exp_tmp_div.items():
        coordinate_exp[key] += count
    
    # そのポリオミノの全パターンを追加
    # coordinate_possible_patern.append(coordinate_possible_patern_poly)

# print(len(coordinate_possible_patern), file=sys.stderr)

### 変更部分
# ある正方形について占う→その期待値を修正，を繰り返す
# 正方形のリストを生成
d = 8
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
        if resp > 0:
            num_times = resp / exp_sum_idx
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune[num] = val_raw * num_times
        ##################### 修正部分 #########################
        else:
            num_times = 0.1
            ## 期待値にかけ直す
            for num in g:
                val_raw = coordinate_exp[num]
                coordinate_exp_fortune[num] = val_raw * num_times

    else:
        pass

# 外した時用に，元々期待値0で，占いで0になったマスのリスト作る
# 元々0のリスト
coordinate_exp_0 = [key for key, value in coordinate_exp.items() if value == 0]
# 占いで0のリスト
coordinate_exp_fortune_0 = [key for key, value in coordinate_exp_fortune.items() if value == 0]
# 差分
possible_miss_list = list(set(coordinate_exp_fortune_0) - set(coordinate_exp_0))

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

# 油田があった時の処理
up_times_poly_include = 10 # セットで存在するマスを上げる
# down_times_poly_exclude = 1 / up_times_poly_include # セットで存在しないマスを下げる
down_times_poly_exclude = 0.5 # セットで存在しないマスを下げる
# 油田がなかった時の処理
up_times_poly_exclude = 10 # セットで存在しないマスを上げる
#down_times_poly_include = 1 / up_times_poly_exclude # セットで存在するマスを下げる
down_times_poly_include = 0.5 # セットで存在するマスを下げる


for _ in range(N*N):
    # 掘る場所の決定（その時一番事後確率が高い座標）
    (i,j) = dig_order[0]
    print("q 1 {} {}".format(i, j))
    resp = int(input())
    print((i,j), resp, file=sys.stderr)
    oil_reserves += resp
    coordinate_exp_fortune[(i,j)] = 0
    #coordinate_next = generate_neighboor_coordinates(i,j,N)
    #coordinate_next_cross = generate_neighboor_coordinates_cross(i,j,N)

    # その座標を含むリストを取得
    #coordinate_include = [x for x in coordinate_possible_patern if (i,j) in x]
    coordinate_include = []
    for x in coordinate_possible_patern:
        if (i,j) in x:
            coordinate_include.extend(x)
    coordinate_include = list(set(coordinate_include))
    # その座標を含まないリストを取得
    #coordinate_exclude = [x for x in coordinate_possible_patern if (i,j) not in x]
    coordinate_exclude = []
    for x in coordinate_possible_patern:
        if (i,j) not in x:
            coordinate_exclude.extend(x)
    coordinate_exclude = list(set(coordinate_exclude))
    #print(coordinate_include, file=sys.stderr)
    #print(coordinate_exclude, file=sys.stderr)

    # 変更部分
    ## 占いの結果によって事後確率を更新
    if resp > 0:
        has_oil.append((i,j))

        # 含むマスを上げる
        for tmp in coordinate_include:
            coordinate_exp_fortune[tmp] = up_times_poly_include * coordinate_exp_fortune[tmp]

        # 含まないマスを下げる
        for tmp in coordinate_exclude:
            coordinate_exp_fortune[tmp] = down_times_poly_exclude * coordinate_exp_fortune[tmp]

        dig_order = list(dict(sorted(coordinate_exp_fortune.items(), key=lambda item: item[1], reverse=True)).keys())
        
        if oil_reserves == oil_grid_num:
            print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
            resp = input()
            # print(resp, file=sys.stderr)
            # assert resp == "1"
            sys.exit()

    else:
        # 含むマスを下げる
        for tmp in coordinate_include:
            coordinate_exp_fortune[tmp] = down_times_poly_include * coordinate_exp_fortune[tmp]
        # 含まないマスを上げる
        for tmp in coordinate_exclude:
            coordinate_exp_fortune[tmp] = up_times_poly_exclude * coordinate_exp_fortune[tmp]
            
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

