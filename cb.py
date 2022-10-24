import random
random.seed(21)

"""These are methods for CBs (comic books). A cb is a list of 
chronologically ordered frames. For the Tic-Tac-Toe example considered in 
this code, a cb is one Tic-Tac-Toe game, and a frame is just one move. For 
example, ['X2', 'O7', 'X6', 'O4', 'X3', 'O8', 'X0'] represents a cb/game and 
'X2' is a frame/move. The X and O refer to the player. X always plays first. 
The numbers refer to the positions on the Tic-Tac-Toe grid, labelled as 
follows: [[0,1, 2], [3,4,5],[6,7,8]]. 

In the general case considered in the arXiv paper, a frame, instead of being 
a single string, can be a list of strings called event descriptors, 
which represent simultaneous events in the frame. """

def cb_has_ended(cb):
    """
    Returns True if cb/game has ended

    Parameters
    ----------
    cb: list[str]

    Returns
    -------
    bool

    """
    if len(cb) == 9:
        return True
    winning_patterns = [
        ['X0', 'X1', 'X2'],
        ['X3', 'X4', 'X5'],
        ['X6', 'X7', 'X8'],
        ['X0', 'X3', 'X6'],
        ['X1', 'X4', 'X7'],
        ['X2', 'X5', 'X8'],
        ['X0', 'X4', 'X8'],
        ['X2', 'X4', 'X6'],
        ['O0', 'O1', 'O2'],
        ['O3', 'O4', 'O5'],
        ['O6', 'O7', 'O8'],
        ['O0', 'O3', 'O6'],
        ['O1', 'O4', 'O7'],
        ['O2', 'O5', 'O8'],
        ['O0', 'O4', 'O8'],
        ['O2', 'O4', 'O6']]

    for pattern in winning_patterns:
        if set(pattern).issubset(set(cb)):
            return True
    return False


def next_frame(incomplete_cb):
    """
    Returns next frame/move for the incomplete cb 'incomplete_cb'. This next
    frame is chosen at random from the remaining possible moves, assuming
    'incomplete_cb' is not an ended game.

    Parameters
    ----------
    incomplete_cb: list[str]

    Returns
    -------
    str

    """
    assert 0 < len(incomplete_cb) < 9
    occupied_spaces = set([int(x[1]) for x in incomplete_cb])
    empty_spaces = set(range(9)) - occupied_spaces
    last_player = incomplete_cb[-1][0]
    if last_player == 'O':
        next_player = 'X'
    elif last_player == 'X':
        next_player = 'O'
    else:
        assert False
    next_space = random.choice(list(empty_spaces))
    return next_player + str(next_space)


def create_cb():
    """
    Returns a cb/game, chosen at random, that is completed (i.e., either one
    player has won or there was a draw.)

    Returns
    -------
    list[str]

    """
    i = random.randrange(9)
    cb = ['X' + str(i)]   # X always first
    while not cb_has_ended(cb):
        cb.append(next_frame(cb))
    return cb


def cb1_is_smaller_that_cb2(cb1, cb2):
    """
    Returns True iff cb1 is smaller than cb2 (cb1 < cb2). As defined in the
    arXiv paper, cb1 < cb2 means cb1 is a proper subset of cb2 and the
    events in cb1 are in the same chronological order as the corresponding
    events in cb2.

    Parameters
    ----------
    cb1: list[str]
    cb2: list[str]

    Returns
    -------
    bool

    """
    if set(cb1) == set(cb2) or set(cb1).issuperset(cb2):
        return False
    cb2_ = [x for x in cb2 if x in cb1]
    return cb1 == cb2_


def cb_already_in_cbLib(cb, cbLib):
    """
    This method returns True iff 'cb' is in 'cbLib'. 'cbLib' is a list (
    i.e., library) of cbs.

    Parameters
    ----------
    cb: list[str]
    cbLib: list[list[str]]

    Returns
    -------
    bool

    """
    for cb1 in cbLib:
        if cb1 == cb:
            return True
    return False


def create_coll_of_cbLibXs(num_created_cbs):
    """
    As defined in the ArXiv paper, 'cbLibX' is a "time compatible library of
    cbs". It's a library of cbs such that the first cb is the largest one of
    the library, and successive cbs of the library are smaller than the
    first one. This method returns a collection ( i.e., list) of cbLibXs.
    This collection is created as follows. Create 'num_created_cbs' cbs
    successively at random. Suppose 'cb' has just been created. If the
    collection is empty, let [cb] be its first cbLibX. If the collection
    already contains some cbLiXs, add 'cb' to all members of the collection
    that will admit it. If none admits it, add the new cbLibX [cb] to the
    collection.

    Parameters
    ----------
    num_created_cbs: int

    Returns
    -------
    list[list[list[str]]

    """
    coll_of_cbLibXs = []
    num_republished_cbs = 0
    for _ in range(num_created_cbs):
        new_cb = create_cb()
        new_cb_has_found_home = False
        if len(coll_of_cbLibXs) == 0:
            coll_of_cbLibXs.append([new_cb])
            new_cb_has_found_home = True
        else:
            for cbLibX in coll_of_cbLibXs:
                if cb_already_in_cbLib(new_cb, cbLibX):
                    num_republished_cbs += 1
                else:
                    if cb1_is_smaller_that_cb2(new_cb, cbLibX[0]):
                        cbLibX.append(new_cb)
                        new_cb_has_found_home = True
        if not new_cb_has_found_home:
            coll_of_cbLibXs.append([new_cb])
    return coll_of_cbLibXs, num_republished_cbs

