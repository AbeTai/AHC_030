"""
任意の大きさの正方形ずつ占う（あまりは長方形で対処）
↓
全ての油田を探し終えた時点で探索をやめるよう変更する
"""

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
import sys

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
print(square_list, file=sys.stderr)

# 油田のマス目の数(重複あり)
tmp = []
for m in range(M):
    tmp.extend(fields[m])
oil_grid_num = len(tmp)


### 占い部分

# 任意のマスずつ占いを使ってみる
# 各行→各列で行い，両方0のマス目は後回しで探索

idx_fortune_over0 = []
idx_fortune_0 = []


d = 3

#d = 2 # 正方形の一辺
coordinates_grouped = extract_squares_coordinates_grouped(N, d) # 占いに渡す座標のリストを生成

for g in coordinates_grouped:
    print("q {} {}".format(len(g), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), g))))
    resp = float(input()) # V(s)の近似値を受け取る
    if resp > 0:
        idx_fortune_over0.append(g)
    else:
        idx_fortune_0.append(g)

#print(idx_fortune_over0, file=sys.stderr)
#print(idx_fortune_0, file=sys.stderr)

# 占いの結果，行列が両方0より大きかったマスを探索
has_oil = []
oil_reserves = 0
for _ in idx_fortune_over0:
    for i,j in _:
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
for _ in idx_fortune_0:
    for i,j in _:
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