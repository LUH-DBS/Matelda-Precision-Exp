import pickle
from pathlib import Path

from raha.raha.sampler import Sampler


class Labeler(Sampler):
    def run(self, dd: Path):

        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "-------------------------------Load State-------------------------------\n"
                  "------------------------------------------------------------------------")
        if dd.exists():
            with dd.open("rb") as state:
                d = pickle.load(state)
        else:
            raise ValueError

        for dataset_tuple in d.labeled_tuples.keys():
            if d.labeled_tuples[dataset_tuple] == 0:
                d.sampled_tuple = dataset_tuple
                if d.has_ground_truth:
                    self.label_with_ground_truth(d)
                else:
                    # TODO implement user dialog
                    pass

        self.save_state(d, dd.name)

if __name__ == "__main__":
    path = Path("../datasets/flights/raha-baran-results-flights/state/2023-05-23 23:38:21.802369").resolve()

    labeler = Labeler()
    labeler.VERBOSE = True
    labeler.run(path)
