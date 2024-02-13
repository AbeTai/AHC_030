"""
最大のポリオミノについて，存在しうる範囲をその形で占う
"""

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
#print(fields, file=sys.stderr)
    
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

### 占い部分

# 最大ポリオミノを特定(座標を格納)
"""
ここでの最大は，面積もしくはピッタリハマる長方形が大きい（左右長*上下長が最大）が考えられる
簡単のため，まずは面積で試す
"""
max_polyomino_num = square_list.index(max(square_list))
max_polyomino = fields[max_polyomino_num]
#print(max_polyomino_num, max_polyomino,file=sys.stderr)

# ポリオミノの並行移動範囲を定義
# xyそれぞれのみ取り出す
max_polyomino_x = max([x[0] for x in max_polyomino])
max_polyomino_y = max([x[1] for x in max_polyomino])
low_move = N - max_polyomino_x
light_move = N - max_polyomino_y
#print(low_move, light_move,file=sys.stderr)

# 占いの結果を格納するリスト
fortune_res = {}

# 一つずつずらしながらポリオミノの形で占う
for low in range(low_move):
    for light in range(light_move):
        # 占いに渡すリスト生成
        fortune_input = [(x[0]+low, x[1]+light) for x in max_polyomino]
        #print(fortune_input,file=sys.stderr)
        print("q {} {}".format(len(fortune_input), ' '.join(map(lambda x: "{} {}".format(x[0], x[1]), fortune_input))))
        resp = float(input())
        #print(resp, file=sys.stderr)
        fortune_res[(f"{low},{light}")] = resp

max_coordinate = max(fortune_res, key = fortune_res.get)
#print(max_coordinate,file=sys.stderr)

# 最大値の場所を掘る
# 掘る座標リストを取得
max_coordinate_spt = max_coordinate.split(",")
low_add, light_add = int(max_coordinate_spt[0]), int(max_coordinate_spt[1])
max_polyomino_verified =  [(x[0]+low_add, x[1]+light_add) for x in max_polyomino]
#max_polyomino_verified
#print(max_polyomino_verified,file=sys.stderr)

# あとのために，占って0だった座標リストも取得しておく
coordinate_fortune_add_0 = [key for key, value in fortune_res.items() if value == 0]
#print(coordinate_fortune_add_0,file=sys.stderr)
coordinate_fortune_0 = []
for add in coordinate_fortune_add_0:
    add_spt = add.split(",")
    low_, light_ = int(add_spt[0]), int(add_spt[1])
    for added in max_polyomino:
        coordinate_fortune_0.append((added[0]+low_, added[1]+light_))
coordinate_fortune_0_dup = list(set(coordinate_fortune_0))
#print(coordinate_fortune_0_dup,file=sys.stderr)

# プールから削除しておく
coordinate_pool = list(set(coordinate_pool) - set(max_polyomino_verified) - set(coordinate_fortune_0_dup))
# 優先順位低いリスト
dig_last = coordinate_fortune_0_dup
print(coordinate_pool,file=sys.stderr)

#print(idx_fortune_over0, file=sys.stderr)
#print(idx_fortune_0, file=sys.stderr)

# 占いの結果，値が最大だった位置を掘る
has_oil = []
oil_reserves = 0

for i,j in max_polyomino_verified:
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
print(oil_reserves,file=sys.stderr)

# プールで残ってる位置を掘る
for i,j in coordinate_pool:
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
print(oil_reserves,file=sys.stderr)