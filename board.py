import time
from collections import deque
import queue
import heapq
import random
from copy import deepcopy

ADJACENT_INDEX = [(1, 3), (0, 2, 4), (1, 5), (0, 4, 6), (1, 3, 5, 7),
                  (2, 4, 8), (3, 7), (4, 6, 8), (5, 7)]

def replace(li, index, index2):
    """
    リスト上で置換を行う
    """
    li = deepcopy(li)
    li[index], li[index2] = li[index2], li[index]
    return li

def random_replace(li, space_index):
    """
    Noneをランダムな位置の要素と置換する
    置換は必ず行われる
    """
    li = deepcopy(li)

    random_index = random.randrange(len(li))
    if random_index is space_index:
        if space_index is 8:
            random_index = 0
        else:
            random_index += 1

    li = replace(li, random_index, space_index)
    return li

def get_space_index(li):
    """
    '空き'のインデックスを返す
    """
    space = None
    return li.index(space)

def shuffle(li):
    """
    Noneと1~8を含む大きさ9のリストを返す
    パズルが解けるようなシャッフルをする
    (8パズルが完成できる ⟺   s を t にする置換のパリティ（偶奇）と「空き」の最短距離の偶奇が等しい)(https://mathtrain.jp/8puzzle)
    """
    li = deepcopy(li)
    distance_is_even = True#完成と初期状態の距離が偶数かどうか
    space_index = get_space_index(li)

    for i in range(30):
        li = random_replace(li, space_index)
        space_index = get_space_index(li)

    shuffled_x = space_index % 3
    shuffled_y = space_index // 3
    distance = abs(0 - shuffled_x) + abs(0 - shuffled_y)#初期と完成のNoneの最短距離
    if distance % 2:
        distance_is_even = False

    if not distance_is_even:
        #距離が奇数だったら、None以外を一回動かして、パリティを奇数にする
        if space_index is not 0 and space_index is not 1:
            replace(li, 0, 1)
        else:
            replace(li, 2, 3)
    return li

def convert_pazzle(board, space_str="x"):
    output = [str(e) for e in [board[:3], board[3:6], board[6:]]]
    text = "\n".join(output).replace("None", space_str)
    return text

def show_pazzle(board, space_str="x"):
    """
    盤面を見やすいように
        3x3の文字列で
        Noneを別の文字に置き換えて
    表示する
    """
    text = convert_pazzle(board, space_str)
    print(text)
    #return text

def play():
    space_str = "#"
    cnt = 0
    end = [e for e in range(1, 9)]
    end.append(None)
    board = shuffle(end)
    directions = {"w":"up", "s":"down", "a":"left", "d":"right"}
    direction_to_number = {"up":-3, "down":3, "left":-1, "right":1}
    show_pazzle(board)
    while True:
        cnt += 1
        space_index = get_space_index(board)
        try:
            direction = directions[input(">>")]
        except KeyError as e:
            print("key error")
            show_pazzle(board)
            continue
        replace_index = space_index + direction_to_number[direction]
        if replace_index in ADJACENT_INDEX[space_index]:
            board = replace(board, space_index, replace_index)
        show_pazzle(board)
        if board == end:
            print("===GAME OVER!!===")
            print("cnt:", cnt)
            break

def show_route(board_dic):
    """
    goalまでたどり着いた盤面を逆にたどっていって、そこまでの経路を表示する
    """
    board_dic = deepcopy(board_dic)
    # step = board_dic['step']
    cnt = 0
    boards = []

    while board_dic["prev"] is not None:
        boards.append(board_dic["board"])
        board_dic = board_dic["prev"]
    boards.append(board_dic["board"])

    boards.reverse()
    for i, board in enumerate(boards):
        print(i)
        show_pazzle(board)
        print()
    print("start:", boards[0])
    # print("step:", step)
    # print("depth:", i)

def show_route2(board_dic):
    """
    goalまでたどり着いた盤面を逆にたどっていって、そこまでの経路をステップ表示する
    """
    board_dic = deepcopy(board_dic)
    step = board_dic['step']
    cnt = 0
    boards = []

    while board_dic["prev"] is not None:
        boards.append(board_dic["board"])
        board_dic = board_dic["prev"]
    boards.append(board_dic["board"])

    boards.reverse()
    while cnt < step:
        print(cnt+1)
        show_pazzle(boards[cnt])
        word = ''
        while word != 'j' and word != 'k':
            word = input()
            if word == 'j':
                cnt += 1
            elif word == 'k':
                if cnt > 0:
                    cnt -= 1
            else:
                print("\u001B[1A", end="")
                print(" "*len(word))
                print("\u001B[1A", end="")
        print("\u001B[5A", end="")

    # for i, board in enumerate(boards):
    #     print(i)
    #     show_pazzle(board)
    #     input()
    #     print("\u001B[5A", end="")

    print()
    print("start:", boards[0])
    # print("step:", step)
    print("depth:", cnt)

def bfs(board=None):
    """
    幅優先探索の実装
    経路もわかるように前の状態の情報を持たせる
    """

    q = queue.Queue()
    checked = []
    cnt = 0
    goal = [e for e in range(1,9)]
    goal.append(None)
    if board is None:
        board = {"board":shuffle(goal), "prev":None}
    show_pazzle(board["board"])
    q.put(board)

    while not q.empty():
        cnt += 1
        if cnt > 181440:
            print("can not find")
            break
        board_dic = q.get()
        board = board_dic["board"]
        print("\r", cnt, board, end="")
        space_index = get_space_index(board)
        if board == goal:
            print("\nend")
            print(board)
            print("cnt:",cnt)
            show_route(board_dic)
            break
        checked.append(str(board))
        adjacents = ADJACENT_INDEX[space_index]
        for adjacent in adjacents:
            board_next = {"board":replace(board, space_index, adjacent),"prev":board_dic}

            if board_dic["prev"] is not None and board_next["board"] == board_dic["prev"]["board"]:
                continue
            if not str(board_next["board"]) in checked:
                q.put(board_next)

def convert_2d_coord(index):
    """
    一次元配列のインデックスからXY座標を返す
    """
    x = index // 3
    y = index % 3
    return x, y

def convert_1d_coord(x,y):
    """
    convert_2d_coordの逆
    """
    index = x * 3 + y
    return index

def get_distance(board, goal):
    """
    盤面を受け取って,それぞれのピースが終了状態のインデックスからどれだけ離れているかという距離の合計値を返す
    距離 = 絶対値(ゴールのインデックス - 現在のインデックス)
    """
    sum_ = 0
    for i, piece in enumerate(board):
        h,w = convert_2d_coord(i)
        gh, gw = convert_2d_coord(goal.index(piece))
        dis = abs(h - gh) + abs(w - gw)
        sum_ += dis
    return sum_

def get_adjacents(index):
    """
    indexの2次元座標的に隣接したindexを返す
    """
    adjacents = []
    x,y = convert_2d_coord(index)
    if x+1 < 3:
        adjacents.append(convert_1d_coord(x+1,y))
    if x-1 >= 0:
        adjacents.append(convert_1d_coord(x-1,y))
    if y+1 < 3:
        adjacents.append(convert_1d_coord(x,y+1))
    if y-1 >= 0:
        adjacents.append(convert_1d_coord(x,y-1))
    return adjacents

def astar(start, goal):
    """
    """
    queue = []
    dist_dic = {}
    checked = {}
    cnt = 0

    start_dic = {'board': start, 'cost': 0, 'prev':None, 'step':0}
    heapq.heappush(queue, (start_dic['cost'], 0, 0, start_dic))
    checked[str(start)] = start_dic
    print(start)

    while len(queue) > 0:
        cnt += 1
        now_board_dic = heapq.heappop(queue)[-1]
        now_board = now_board_dic['board']
        print("\r", cnt, now_board, end="")
        if now_board == goal:
            print("end")
            return now_board_dic
        space_index = get_space_index(now_board_dic['board'])
        adjacents = get_adjacents(space_index)
        for i, adjacent in enumerate(adjacents):
            new_board = replace(now_board, space_index, adjacent)
            new_step = now_board_dic['step']+1
            new_cost = new_step+get_distance(new_board, goal)
            new_board_dic = {'board':new_board, 'cost':new_cost, 'prev':now_board_dic, 'step':new_step}

            if str(new_board) not in checked or new_cost < checked[str(new_board)]['cost']:
                checked[str(new_board)] = new_board_dic
                heapq.heappush(queue, (new_cost, cnt, i, new_board_dic))
    print(queue)
    raise Exception("終わった！")




if __name__ == '__main__':
    #play()

    goal = [1,2,3,8,None,4,7,6,5]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, None]
    start = shuffle(goal)
    start = [8,6,7,2,5,4,3,None,1]

    start_time = time.time()
    result = astar(start, goal)
    e_time = time.time() - start_time
    print("step:", result['step'])
    show_route2(result)
    print ("e_time: {0}".format(e_time) + "[s]")
