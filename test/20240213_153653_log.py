"""
任意の大きさの正方形ずつ占う（あまりは長方形で対処）
↓
掘る
↓
占う
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
#print(square_list, file=sys.stderr)

# 油田のマス目の数(重複あり)
tmp = []
for m in range(M):
    tmp.extend(fields[m])
oil_grid_num = len(tmp)

### 占い&掘る部分

# 占いの結果，行列が両方0より大きかったマスを探索
has_oil = []
oil_reserves = 0

#idx_fortune_over0 = []
idx_fortune_0 = []

if max(square_list) <= 10:
    d = 2
else:
    d = 3

coordinates_grouped = extract_squares_coordinates_grouped(N, d) # 占いに渡す座標のリストを生成

for g in coordinates_grouped:
    #print(g, file = sys.stderr)
    print("q {} {}".format(len(g), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), g))))
    resp = float(input()) # V(s)の近似値を受け取る
    if resp > 0:
        #idx_fortune_over0.append(g)
        # 逐次的に掘る
        for g_dev in g:
            # print(g_dev, file = sys.stderr)
            print("q 1 {} {}".format(g_dev[0], g_dev[1]))
            resp_ = int(input())
            if resp_  > 0:
                oil_reserves += resp_
                has_oil.append(g_dev)

            if oil_reserves == oil_grid_num:
                print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
                resp = input()
                # print(resp, file=sys.stderr)
                # assert resp == "1"
                sys.exit()

    else:
        idx_fortune_0.extend(g) # 外した場合用

#print(idx_fortune_over0, file=sys.stderr)
#print(idx_fortune_0, file=sys.stderr)


#print("fortune miss", file=sys.stderr)

for g_dev_ in idx_fortune_0:
    print("q 1 {} {}".format(g_dev_[0], g_dev_[1]))
    resp = int(input())
    # print(resp,oil_reserves, file=sys.stderr)

    if resp > 0:
        oil_reserves += resp
        has_oil.append(g_dev_)

    if oil_reserves == oil_grid_num:
        print("a {} {}".format(len(has_oil), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), has_oil))))
        resp = input()
        # print(resp, file=sys.stderr)
        # assert resp == "1"
        sys.exit()