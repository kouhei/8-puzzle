import time
import queue
import random
from copy import deepcopy

ADJACENT_INDEX = [(1, 3), (0, 2, 4), (1, 5), (0, 4, 6), (1, 3, 5, 7),
                  (2, 4, 8), (3, 7), (4, 6, 8), (5, 7)]

board = []

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

def bfs(board=None):
    """
    幅優先探索の実装
    """
    
    q = queue.Queue()
    checked = []
    cnt = 0
    goal = [e for e in range(1,9)]
    goal.append(None)
    goal = goal
    if board is None:
        board = shuffle(goal)
    show_pazzle(board)
    q.put(board)
    while True:
        cnt += 1
        #print(cnt)
        board = q.get()
        #show_pazzle(board)
        print("\r",cnt,board, end="")
        space_index = get_space_index(board)
        if board == goal:
            print("\nend")
            print(board)
            print("cnt:",cnt)
            break
        checked.append(str(board))
        adjacents = ADJACENT_INDEX[space_index]
        for adjacent in adjacents:
            board_next = replace(board, space_index, adjacent)
            if not str(board_next) in checked:
                q.put(board_next)



if __name__ == '__main__':
    #play()
    #bfs([1,None,2,4,5,3,7,8,6])

    start = time.time()
    #bfs([None,4,6,5,1,2,7,8,3])
    #bfs([7,1,6,3,4,8,None,2,5])
    bfs([1,2,3,4,6,5,7,8,None])
    e_time = time.time() - start
    print ("e_time:{0}".format(e_time) + "[s]")
