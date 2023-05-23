import pickle
from pathlib import Path

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
    path = Path("../datasets/flights/raha-baran-results-flights/state/2023-05-18 00:59:06.417399").resolve()
    print(path)
