


"""

"""

from state import State
from play import shuffle
from copy import deepcopy

end = State([1,2,3,4,5,6,7,8,None])
#state = State([1,2,3,4,5,6,7,None,8])
state = State([None,1,2,3,4,5,6,7,8])
#state = State(shuffle(1))
#state.prev = state

checked = [state]
queue = [state]
cnt = 0
#prev_state = deepcopy(state)
is_end = False
while True:
    cnt += 1
    for q in queue:
        #print(q)
        if end == q:
            print("END!!!")
            q.show()
            is_end = True
            
    if is_end:
        break

    state = deepcopy(queue.pop(0))
    state.show()

    prev_state = deepcopy(state)
    for adjacent in state.ADJACENT_INDEX[state.space]:
        state.move(adjacent)
        if state not in checked:
            print("add")
            #state.show()
            queue.append(state)
            checked.append(state)
        state = deepcopy(prev_state)

#print(adjacents)
print(cnt)
