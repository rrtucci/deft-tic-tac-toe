import pprint
from itertools import product
import numpy as np
import pandas as pd


class BayesNet:
    """
    This class builds a Bayesian Network (bnet) from a DAG (encoded in
    'arrows') and a dataset (encoded in 'dataset_df').

    Attributes
    ----------
    arrows: list[(str,str)]
        This is a list of the arrows of the DAG. An arrow in a pair of
        node names.
    dataset_df: pd.DataFrame
        A pandas DataFrame wherein the columns are the node names and the rows
        are integers that label DAGs in a cbLibX.
    nd_to_TPM: dict[str, dict()]
        dictionary mapping node name to TPM (transition probability matrix)
        of the node.
    nd_to_parents: dict[str, list[str]]
        dictionary mapping node to list of parents.
    nodes: list[str]
        list of all node names of DAG

    """

    def __init__(self, arrows, dataset_df):
        """

        Parameters
        ----------
        arrows: list[(str,str)]
        dataset_df: pd.DataFrame
        """
        self.arrows = arrows
        self.dataset_df = dataset_df
        self.nodes = []
        self.nd_to_parents = {}
        self.nd_to_TPM = {}
        for arrow in arrows:
            for i in [0, 1]:
                if arrow[i] not in self.nodes:
                    self.nodes.append(arrow[i])
        self.nd_to_parents = {nd: [] for nd in self.nodes}
        for arrow in arrows:
            for nd in self.nodes:
                # print("nnbbcc", arrow, nd)
                if arrow[1] == nd:
                    if arrow[0] not in self.nd_to_parents[nd]:
                        self.nd_to_parents[nd].append(arrow[0])
        # print("llkkjj", self.nd_to_parents)
        for nd in self.nodes:
            self.nd_to_TPM[nd] = self.get_TPM(nd)

    def get_TPM(self, nd):
        """
        This method returns the empirical TPM for the node 'nd'. The TPM is
        expressed as a dictionary mapping a binary n-tuple representing a
        state of the parents to a pair of floats that add to 1 and give the
        probability of the node 'nd' being in state 0 for the first float
        and state 1 for the second float.

        Parameters
        ----------
        nd: str

        Returns
        -------
        pa_st_to_prob_of_nd_st: dict(tuple(str), np.array[float, float])

        """
        num_parents = len(self.nd_to_parents[nd])
        num_rows = len(self.dataset_df.index)
        # product() iterator destroyed after first use
        pa_sts = list(product((0, 1), repeat=num_parents))
        pa_st_to_prob_of_nd_st = {pa_st: np.zeros((2,))
                                  for pa_st in pa_sts}
        den_indi_fun = {pa_st: np.zeros((2,))
                        for pa_st in pa_sts}
        num_ind_fun = {pa_st: np.zeros((2,))
                       for pa_st in pa_sts}
        for pa_st in pa_sts:
            for nd_st in [0, 1]:
                for row in range(num_rows):
                    # print("ccdff", nd_st)
                    parents = self.nd_to_parents[nd]
                    bool_list = [pa_st[parents.index(pa_nd)]
                                 == self.dataset_df.loc[row, pa_nd] for
                                 pa_nd in self.nd_to_parents[nd]]
                    # print("kkjju", bool_list)
                    if len(bool_list) != 0:
                        den_indi_fun[pa_st][nd_st] += int(all(bool_list))
                    # list1.append() returns None
                    bool_list.append(nd_st == self.dataset_df.loc[row, nd])
                    # print("9999", bool_list)
                    num_ind_fun[pa_st][nd_st] += int(all(bool_list))
        for nd_st in [0, 1]:
            if len(pa_sts) == 0:
                pa_st_to_prob_of_nd_st[tuple()][nd_st] =\
                    num_ind_fun[tuple()][nd_st]
            for pa_st in pa_sts:
                pa_st_to_prob_of_nd_st[pa_st][nd_st] = \
                    num_ind_fun[pa_st][nd_st]/den_indi_fun[pa_st][nd_st]
        return pa_st_to_prob_of_nd_st

    def print(self):
        """
        This method prints a description of the bnet. The description
        contains, for each node of the bnet, its name, the name of its
        parents, and its empirical TPM.

        Returns
        -------
        None

        """
        for nd in self.nodes:
            print("\nnode:", nd)
            print("parents:", self.nd_to_parents[nd])
            pprint.pprint(self.nd_to_TPM[nd])
