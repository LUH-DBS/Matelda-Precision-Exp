import os
import datetime
import pickle
from pathlib import Path

from raha import raha
from raha.raha import Detection


class Sampler(Detection):

    def save_state(self, d, name=None):
        pickle_path = Path(d.results_folder).resolve().joinpath(f"state").resolve()
        if not pickle_path.exists():
            pickle_path.mkdir()

        file_name = str(datetime.datetime.now()) if name is None else name
        pickle_path = pickle_path.joinpath(file_name)
        pickle_path.touch()
        with pickle_path.open(mode='wb') as file:
            pickle.dump(d, file)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "------------------------------Stored state------------------------------\n"
                  "------------------------------------------------------------------------")

    def run(self, dd):
        """
        This method runs Raha on an input dataset to detection data errors.
        """
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "---------------------Initializing the Dataset Object--------------------\n"
                  "------------------------------------------------------------------------")
        d = self.initialize_dataset(dd)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "-------------------Running Error Detection Strategies-------------------\n"
                  "------------------------------------------------------------------------")
        self.run_strategies(d)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "-----------------------Generating Feature Vectors-----------------------\n"
                  "------------------------------------------------------------------------")
        self.generate_features(d)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "---------------Building the Hierarchical Clustering Model---------------\n"
                  "------------------------------------------------------------------------")
        self.build_clusters(d)
        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "-------------Iterative Clustering-Based Sampling and Labeling-----------\n"
                  "------------------------------------------------------------------------")

        while len(d.labeled_tuples) < self.LABELING_BUDGET:
            self.sample_tuple(d)
            d.labeled_tuples[d.sampled_tuple] = 0
            for j in range(d.dataframe.shape[1]):
                cell = (d.sampled_tuple, j)
                d.labeled_cells[cell] = [0]
            if self.VERBOSE:
                print("------------------------------------------------------------------------")

        print(d.labeled_tuples)
        self.save_state(d)


########################################


########################################
if __name__ == "__main__":
    dataset_name = "flights"
    dataset_dictionary = {
        "name": dataset_name,
        "path": os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "dirty.csv")),
        "clean_path": os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "datasets", dataset_name, "clean.csv"))
    }
    app = Sampler()
    app.VERBOSE = True
    app.run(dataset_dictionary)
