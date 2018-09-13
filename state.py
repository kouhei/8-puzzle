class State():

    ADJACENT_INDEX = [(1,3), (0, 2, 4), (1, 5), (0, 4, 6), (1, 3, 5, 7),
                      (2, 4, 8), (3, 7), (4, 6, 8), (5, 7)]
    #↑ 隣接ピースのインデックス
    #ADJACENT_INDEX[0] == インデックスが0のピースに隣接するピース
    def __init__(self, board, space, prev):
        self.board = board#盤面を表す一次元の配列(空白の場所はNone)
        self.space = space#空白の位置(boardのインデックス)
        self.prev = prev#前の状態(移動前のState)

    def get_pos(self, piece):
        """
        piece(そのピースに書かれている番号)を受け取り、
        そのピースの現在のインデックスを返す
        args:
            piece: int 1~8
        return:
            index: int 0~8
        """
        for i, piece_num in enumerate(self.board):
            if piece_num is piece:
                return i


    def exist_space_next_to(self, pos):
        """
        ピースのインデックスを受け取り、
        その隣にspaceが存在するか(その駒が動かせるかどうか)

        args:
            pos: int 0~8
        return:
            exist_space_next_to_piece: Bool
        """
        for adjacent in self.ADJACENT_INDEX[pos]:
            if adjacent is self.space:
                return True
        return False


    def move(self, piece):
        """
        pieceを動かす

        動かせるかどうかの確認:
            そのピースの隣にspaceがあるか

        args:
            piece: int 1~8
        return:
            void
        """
        piece_pos = self.get_pos(piece)
        
        if not self.exist_space_next_to(piece_pos):
            return None

        self.board[piece_pos], self.board[self.space] = self.board[self.space], self.board[piece_pos]

    def show(self):
        """
        盤面を出力する
        args:
            None
        return:
            None
        """
        none_str = "#"
        outputs = [self.board[:3], self.board[3:6], self.board[6:]]
        outputs = [str(o) for o in outputs]
        for output in outputs:
            output = output.replace("None", none_str)
            print(output)

if __name__ == "__main__":
    st = State([1,2,3,4,5,6,7,8,None], 8, [None for _ in range(9)])
    st.show()
    print()
    st.move(8)
    st.show()

