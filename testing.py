from cb import *
from latex_rendering import *
from dot import *
from BayesNet import *

from graphviz import Source
import pprint
import pandas as pd


def test1():
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
    for cbLibX in coll_of_cbLibXs:
        if len(cbLibX) == max_len:
            print(k, ":")
            print(cbLibX)
            print()
            k += 1


def test3(draw=True, memory_time=2):
    """

    Parameters
    ----------
    draw: bool
    memory_time: int

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
    if draw:
        latex = cb_list_to_latex(cbLibX, 4)
        draw_latex_str(latex)
    all_arrows = []
    all_dots = 'digraph {\n'
    for i, cb in enumerate(cbLibX):
        dot, arrows = dot_for_cb(cb,
                                 memory_time,
                                 graph_name=str(i),
                                 is_subgraph=True)
        print(dot)
        print(arrows)
        all_dots += dot
        all_arrows += arrows
        if i == len(cbLibX)-1:
            all_dots += " }"
            print(all_dots)
            if draw:
                s = Source(all_dots,
                           filename="cbLibX.gv",
                           format="png")
                s.view()
    print("all_arrows_list=", all_arrows)
    arrow_to_freq = {}
    for arrow in all_arrows:
        if arrow in arrow_to_freq.keys():
            arrow_to_freq[arrow] += 1
        else:
            arrow_to_freq[arrow] = 1
    print("arrow frequencies dictionary:")
    pprint.pprint(arrow_to_freq)
    dot_hfa, arrows_hfa = dot_for_high_freq_arrows_DAG(arrow_to_freq, 2)
    print("dot for hfa DAG:\n", dot_hfa)
    if draw:
        s = Source(dot_hfa,
                   filename="G_hfa.gv",
                   format="png")
        s.view()
    dataset = {}
    for event_i, event in enumerate(cbLibX[0]):
        dataset[event] = [0]*len(cbLibX)
    for cb_i, cb in enumerate(cbLibX):
        for event_i, event in enumerate(cbLibX[0]):
            if event in cb:
                dataset[event][cb_i] = 1
    pprint.pprint(dataset)
    dataset_df = pd.DataFrame(dataset)
    print(dataset_df)
    bnet_hfa = BayesNet(arrows_hfa, dataset_df)
    bnet_hfa.print()


if __name__ == "__main__":
    test1()
    # test2()
    # test3()
    # test3(draw=False, memory_time=2)



        










