import os
import pickle
from pathlib import Path

from raha import raha
from raha.raha import Detection


class Predictor(Detection):

    def run(self, dd: Path):
        if dd.exists():
            with dd.open("rb") as state:
                d = pickle.load(state)
        else:
            raise ValueError

        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "--------------Propagating User Labels Through the Clusters--------------\n"
                  "------------------------------------------------------------------------")
        self.propagate_labels(d)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "---------------Training and Testing Classification Models---------------\n"
                  "------------------------------------------------------------------------")
        self.predict_labels(d)
        if self.SAVE_RESULTS:
            if self.VERBOSE:
                print("------------------------------------------------------------------------\n"
                      "---------------------------Storing the Results--------------------------\n"
                      "------------------------------------------------------------------------")
        self.store_results(d)
        return d.detected_cells


if __name__ == "__main__":
    path = Path("../datasets/flights/raha-baran-results-flights/state/2023-05-23 23:38:21.802369").resolve()

    predictor = Predictor()
    predictor.VERBOSE = True
    detection_dictionary = predictor.run(path)

    dataset_name = "flights"
    dataset_dictionary = {
        "name": dataset_name,
        "path": os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "dirty.csv")),
        "clean_path": os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "clean.csv"))
    }

    data = raha.dataset.Dataset(dataset_dictionary)
    p, r, f = data.get_data_cleaning_evaluation(detection_dictionary)[:3]
    print("Raha's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))
