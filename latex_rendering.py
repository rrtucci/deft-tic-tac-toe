import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['text.usetex'] = True

"""A very convenient way to draw a Tic-Tac-Toe game is to create a latex 
string for a table in the tabular environment. Then render the latex string 
using matplotlib. """


def cb_to_latex(cb):
    """
    This method returns a latex string representing a cb/Tic-Tac-Toe game.
    The time each X or O is played is indicated by the time enclosed in
    parenthesis. For example, X3(2) is an X played at time 2 and position 3.
    The 3, which indicates the position on the grid, is redundant and
    omitted if X3(2)'s position is indicated by placing it on the grid.

    Parameters
    ----------
    cb: list[str]

    Returns
    -------
    str

    """
    latex = r"\setlength\arrayrulewidth{2pt}" \
            r"\begin{tabular}{c|c|c}" \
            r"00&11&22\\\hline " \
            r"33&44&55\\\hline " \
            r"66&77&88\end{tabular}"
    used_pos = []
    for time, frame in enumerate(cb):
        letter = frame[0]
        pos = frame[1]
        new_str = letter + '(' + str(time) + ')'
        # print("nnmmmkk", time, frame, new_str)
        latex = latex.replace(pos*2, new_str)
        used_pos.append(int(pos))
    unused_pos = [str(i) for i in range(9) if i not in used_pos]
    for pos in unused_pos:
        latex = latex.replace(pos*2, '')
    return latex


def cb_list_to_latex(cb_list, nmax):
    """
    This method uses the method 'cb_to_latex()' to produce a latex string
    for each cb in a list 'cb_list'. Then it splices the latex of each cb
    into a latex string for all the cbs in 'cb_list'. Only 0< len(cb_list)
    <= nmax is allowed.

    Parameters
    ----------
    cb_list: list[list[str]]
    nmax: int

    Returns
    -------

    """
    n = len(cb_list)
    assert 0 < n <= nmax
    latex = r"\begin{tabular}"
    latex += "{" + "c" * nmax + "}"
    for pos, cb in enumerate(cb_list):
        latex += cb_to_latex(cb)
        if pos != n-1:
            latex += "&"
    if n < nmax:
        latex += "&"*(nmax - n)
    latex += r"\end{tabular}"
    return latex


def draw_latex_str(latex):
    # https://stackoverflow.com/questions/38168292/
    # render-latex-text-with-python
    """
    This method renders the latex string 'latex' using matplotlib.

    Parameters
    ----------
    latex: str

    Returns
    -------
    None

    """
    plt.figure(figsize=(8, .8))
    plt.text(0.5, 0.5, latex,
             fontsize=9,
             horizontalalignment='center')
    plt.axis('off')

    plt.show()
