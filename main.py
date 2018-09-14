"""
とりあえず、CUIで人間がプレイできるようにする
"""
import random
from state import State
def shuffle(seed=None):
    """
    Noneと1~8を含む大きさ9のリストを返す
    args:
        seed: None or int (乱数シード)
    return:
        board list: list (None or int 1~8)
    """
    li = list(range(9))

    if seed is not None:
        random.seed(seed)

    random_list = random.sample(li, len(li))
    board_list = [None if e is 0 else e for e in random_list]
    return board_list

def play():
    """
    標準入力で動かしたい駒の数字を受け取り、それを動かす
    args:
        None
    return:
        None
    """
    board = shuffle()
    puzzle = State(board)
    is_done = False
    puzzle.show()
    while(not is_done):
        try:
            #piece = int(input("動かしたい駒を入力してください: "))
            directs = {"w":"up", "s":"down", "a":"left", "d":"right"}
            direct_key = input("動かしたい方向を入力してください")

            #if not 0 < piece < 9:
            if not direct_key in directs:
                raise ValueError()
        except ValueError as e:
            #print("[ERROR]駒は1~8の整数で入力してください")
            print("[ERROR]方向を入力してください")
            continue

        direct = directs[direct_key]
        #puzzle.move_by_piece(piece)
        puzzle.move_by_direction(direct)
        puzzle.show()

        if puzzle.board == [1,2,3,4,5,6,7,8,None]:
            is_done = True


if __name__ == '__main__':
    #print(shuffle())
    #print(shuffle(0))
    play()
