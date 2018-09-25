import time
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

def show_pazzle(board, space_str="#"):
    """
    盤面を見やすいように
        3x3の文字列で
        Noneを別の文字に置き換えて
    表示する
    """
    output = [str(e) for e in [board[:3], board[3:6], board[6:]]]
    text = "\n".join(output).replace("None", space_str)
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
    cnt = 0
    while board_dic["prev"] is not None:
        cnt += 1
        print(cnt)
        show_pazzle(board_dic["board"])
        print()
        board_dic = board_dic["prev"]

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

def index_to_2Dindex(index):
    """
    """
    h = index // 3
    w = index % 3
    return (h,w)

def get_distance(board):
    """
    盤面を受け取って,それぞれのピースが終了状態のインデックスからどれだけ離れているかという距離の合計値を返す
    距離 = 絶対値(ゴールのインデックス - 現在のインデックス)
    """
    goal = [1,2,3,4,5,6,7,8,None]
    sum = 0
    for i, piece in enumerate(board):
        h,w = index_to_2Dindex(i)
        gh, gw = index_to_2Dindex(goal.index(piece))
        dis = abs(h - gh) + abs(w - gw)
        sum += dis
    return sum

def a_star_search(board=None):
    """
    A*アルゴリズムの実装
        ゴールの位置からの距離の合計で優先度を決定する
    経路もわかるように前の状態の情報を持たせる
    """
    hq = []
    checked = []
    cnt = 0
    goal = [1,2,3,4,5,6,7,8,None]
    if board is None:
        board = {"board":shuffle(goal), "prev":None, "num":0}
    show_pazzle(board["board"])
    start_distance = get_distance(board["board"])
    heapq.heappush(hq, (board["num"], start_distance, 0, 0, board))

    while cnt < 181441:
        cnt += 1
        board_dic = heapq.heappop(hq)[-1]
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
        for i,adjacent in enumerate(adjacents):
            board_next = {"board":replace(board, space_index, adjacent),"prev":board_dic, "num":board_dic["num"]+1}

            if board_dic["prev"] is not None and board_next["board"] == board_dic["prev"]["board"]:
                continue
            if not str(board_next["board"]) in checked:
                heapq.heappush(hq, (board_next["num"]+get_distance(board_next["board"]), cnt, i, board_next))
    print("can not find")


if __name__ == '__main__':
    #play()
    #bfs([1,None,2,4,5,3,7,8,6])

    start = time.time()
    #bfs({"board":[None,4,6,5,1,2,7,8,3],"prev":None})
    #bfs({"board":[7,1,6,3,4,8,None,2,5], "prev":None})
    #bfs({"board":[1,2,3,4,6,5,7,8,None],"prev":None})
    #bfs()
    #a_star_search({"board":[None,4,6,5,1,2,7,8,3],"prev":None, "num":0})
    #a_star_search({"board":[7,1,6,3,4,8,None,2,5], "prev":None, "num":0})
    #a_star_search({"board":[8,6,7,2,5,4,3,None,1], "prev":None, "num":0})
    #a_star_search({"board":[6,4,7,8,5,None,3,2,1],"prev":None,"num":0})
    a_star_search()

    e_time = time.time() - start
    print ("e_time:{0}".format(e_time) + "[s]")
