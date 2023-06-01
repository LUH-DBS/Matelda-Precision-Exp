import pickle
from pathlib import Path

from raha.raha.sampler import Sampler


class Labeler(Sampler):
    def calc_number_of_labels(self, d):
        k = len(d.labeled_tuples) + 1
        print(d.labeled_tuples)

        for j in range(d.dataframe.shape[1]):
            for c in d.clusters_k_j_c_ce[k][j]:
                d.labels_per_cluster[(j, c)] = {cell: d.labeled_cells[cell][0] for cell in d.clusters_k_j_c_ce[k][j][c]
                                                if
                                                cell[0] in d.labeled_tuples}

    def run(self, d):

        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "-------------------------------Load State-------------------------------\n"
                  "------------------------------------------------------------------------")

        dataset_tuples = d.labeled_tuples.keys()
        for dataset_tuple in dataset_tuples:
            d.sampled_tuple = dataset_tuple
            if d.has_ground_truth:
                self.label_with_ground_truth(d)
            else:
                # TODO implement user dialog
                pass
        self.calc_number_of_labels(d)
        return d


if __name__ == "__main__":
    path = Path("../datasets/flights/raha-baran-results-flights/state/2023-06-01 14:01:26.267208").resolve()

    labeler = Labeler()
    dd = labeler.load_state(path)
    labeler.VERBOSE = True
    detection_dictionary = labeler.run(dd)

    labeler.save_state(detection_dictionary, path.name)
