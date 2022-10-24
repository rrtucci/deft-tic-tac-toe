from cb import *
from latex_rendering import *
from dot import *
from BayesNet import *

import pprint
import pandas as pd


def test1():
    """

    Returns
    -------
    None

    """
    cb_list = []
    for _ in range(5):
        cb = create_cb()
        print(cb)
        cb_list.append(cb)

    cb = create_cb()
    latex = cb_to_latex(cb)
    print(cb)
    print(latex)
    draw_latex_str(latex)

    latex = cb_list_to_latex(cb_list, 6)
    print(latex)
    draw_latex_str(latex)


def test2(num_created_cbs=2000):
    """
    This method creates a number 'num_created_cbs' of cbs at random using
    cb.create_cb()'. Since the cb are created at random, sometimes the same
    cb is created more than once. Repeated cbs are counted and their final
    number 'num_republished_cbs' is printed. The method inserts all the
    created cbs into a collection of cbLiXs. A description of the final
    state of the collection of cbLiXs is printed.

    Parameters
    ----------
    num_created_cbs: int

    Returns
    -------
    None

    """
    coll_of_cbLibXs, num_republished_cbs = \
        create_coll_of_cbLibXs(num_created_cbs)
    print("number of republished cbs=", num_republished_cbs)
    print("number of cbLibXs=", len(coll_of_cbLibXs))
    len_list = [len(x) for x in coll_of_cbLibXs]
    max_len = max(len_list)
    print("lengths of cbLibXs:")
    for x in range(max_len):
        print("len=", x+1, ", count=", len_list.count(x+1))
    k = 1
    print("cbLibXs of maximum length:")
    for cbLibX in coll_of_cbLibXs:
        if len(cbLibX) == max_len:
            print(k, ":")
            print(cbLibX)
            print()
            k += 1


def test3(draw=True,
          memory_time=2,
          verbose=True,
          j_embed=False):
    """

    Parameters
    ----------
    draw: bool
    memory_time: int
    verbose: bool
    j_embed: bool
        True iff want to embed image in jupyter notebook. If you are using a
        python terminal instead of a jupyter notebook, only j_embed=False
        will draw image.

    Returns
    -------
    None

    """
    cbLibX = \
        [
            ['X2', 'O5', 'X7', 'O1', 'X4', 'O0', 'X8', 'O3', 'X6'],
            ['X2', 'O5', 'X4', 'O3', 'X6'],
            ['X7', 'O1', 'X8', 'O3', 'X6'],
            ['X2', 'O1', 'X4', 'O0', 'X6']
        ]
    print("Consider the following cbLibX:")
    pprint.pprint(cbLibX)
    if draw:
        print("cbLibX rendered on Tic-Tac-Toe grids:")
        latex = cb_list_to_latex(cbLibX, 4)
        draw_latex_str(latex)
    all_arrows = []
    all_dots = 'digraph {\n'
    for i, cb in enumerate(cbLibX):
        dot, arrows = dot_for_cb(cb,
                                 memory_time,
                                 graph_name=str(i),
                                 is_subgraph=True)
        if verbose:
            print(dot)
            print(arrows)
        all_dots += dot
        all_arrows += arrows
        if i == len(cbLibX)-1:
            all_dots += " }"
            if verbose:
                print(all_dots)
            if draw:
                print("DAG for each cb in cbLibX "
                      "with memory_time=" + str(memory_time) + ":")
                s = gv.Source(all_dots,
                           filename="cbLibX.gv",
                           format="png")

                draw_dot(s, j_embed)
    if verbose:
        print("all_arrows_list=", all_arrows)
    arrow_to_freq = {}
    for arrow in all_arrows:
        if arrow in arrow_to_freq.keys():
            arrow_to_freq[arrow] += 1
        else:
            arrow_to_freq[arrow] = 1
    print("arrow frequencies dictionary:")
    pprint.pprint(arrow_to_freq)
    arr_rep_th = 2
    dot_hfa, arrows_hfa = dot_for_high_freq_arrows_DAG(
        arrow_to_freq, arr_rep_th)
    if verbose:
        print("dot for hfa DAG:\n", dot_hfa)
    if draw:
        print("high frequency arrows (hfa) DAG"
              " with arrow repetition threshold=" + str(arr_rep_th) + ":")
        s = gv.Source(dot_hfa,
                   filename="G_hfa.gv",
                   format="png")
        draw_dot(s, j_embed)
    dataset = {}
    for event_i, event in enumerate(cbLibX[0]):
        dataset[event] = [0]*len(cbLibX)
    for cb_i, cb in enumerate(cbLibX):
        for event_i, event in enumerate(cbLibX[0]):
            if event in cb:
                dataset[event][cb_i] = 1
    if verbose:
        pprint.pprint(dataset)
    dataset_df = pd.DataFrame(dataset)
    print("dataset as pandas DataFrame:")
    print(dataset_df)
    bnet_hfa = BayesNet(arrows_hfa, dataset_df)
    print("hfa DAG upgraded to bnet:")
    bnet_hfa.print()


if __name__ == "__main__":
    test1()
    # test2()
    # test3(draw=True,
    #       memory_time=2,
    #       verbose=False,
    #       j_embed=False)



        










