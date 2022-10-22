"""dot is the language used by graphviz."""

def dot_for_cb(cb, memory_time, graph_name='', is_subgraph=False):
    """
    This method returns a dot string describing a DAG. It also returns a
    list of the arrows of the DAG. The DAG is created from 'cb' as follows.
    For every event e in cb, we draw arrows e1->e, where e1 occurs a time 1,
    2, ..., memory_time-1, memory_time earlier e.

    Parameters
    ----------
    cb: list[str]
    memory_time: int
    graph_name: str
    is_subgraph: bool

    Returns
    -------
    str, list[(str, str)]

    """
    arrows = []
    if is_subgraph:
        dot = "subgraph {\n"
    else:
        dot = "digraph {\n"
    for event_i, event in enumerate(cb):
        for delta in range(memory_time):
            j = event_i - delta - 1
            if j >= 0:
                arrows.append((cb[j], event))
                if not is_subgraph:
                    dot += cb[j] + " -> " + event + ';\n'
                else:
                    dot += cb[j] + "_" + graph_name + \
                           " -> " + \
                           event + "_" + graph_name + ';\n'

    dot += "}\n"
    return dot, arrows


def dot_for_high_freq_arrows_DAG(arrow_freq_dict, N_hfa):
    """
    This method constructs what is called the "high frequency arrows DAG"
    for a particular cbLibX. It returns the dot string describing this
    DAG. It also returns a list of the arrows in the DAG.

    Each cb in a cbLibX has a DAG, and that DAG can be described by the set
    of all its arrows, call it A_cb. If we make a list of all the arrows in
    all the A_cb, and map each arrow to the number of times it occurs in all
    the A_cb, we get the arrow frequency dictionary 'arrow_freq_dict'.

    In constructing the dot/DAG returned by this method, we keep only arrows
    with a repetition number greater or equal to N_hfa.

    Parameters
    ----------
    arrow_freq_dict: dict[(str,str), int]

    N_hfa: int

    Returns
    -------
    str, list[(str, str)]

    """
    arrows = []
    dot = "digraph {\n"
    for arrow, freq in arrow_freq_dict.items():
        if freq >= N_hfa:
            arrows.append(arrow)
            dot += arrow[0] + " -> " + arrow[1] + \
                ' [label=' + str(freq) + "];\n"
    dot += "}\n"
    return dot, arrows
