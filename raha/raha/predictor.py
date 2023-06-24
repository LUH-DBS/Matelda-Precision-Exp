import json
import os
import pickle
from pathlib import Path

from raha import raha

from raha.raha import Detection
from raha.raha.sampler import Sampler


class Predictor(Sampler):

    def run(self, d):

        if self.VERBOSE:
            print("------------------------------------------------------------------------\n"
                  "--------------Propagating User Labels Through the Clusters--------------\n"
                  "------------------------------------------------------------------------")
        print(d)
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
        return d


if __name__ == "__main__":
    path = Path("../datasets/flights/raha-baran-results-flights/state/2023-06-01 15:02:28.343942").resolve()
    dataset_path = "../datasets/flights"
    dataset_name = "flights"
    execution_number = 1 # we should change this if we need to run each dataset 10 times
    labeling_budget = 20 
    results_path = "../datasets/flights/results"
    
    predictor = Predictor()
    dd = predictor.load_state(path)

    predictor.VERBOSE = True
    d = predictor.run(dd)
    detection_dictionary, labeled_cells, actuall_errors_dict = d.detected_cells, d.labeled_cells, d.get_actual_errors_dictionary()

    dataset_dictionary = dd.dictionary

    data = raha.dataset.Dataset(dataset_dictionary)
    detected_errors = list(detection_dictionary.keys())
    metrics = data.get_data_cleaning_evaluation(detection_dictionary)
    results = {'dataset_path': dataset_path, 'dataset_name': dataset_name, 'execution_number': execution_number, 'dataset_shape': data.dataframe.shape, 
               'precision': metrics["ed_p"], 'recall': metrics["ed_r"], 'f_score': metrics["ed_f"],
               'tp': metrics["ed_tp"], 'ed_tpfp': metrics["output_size"], 'ed_tpfn': metrics["actual_errors"],
               'number_of_labeled_tuples': labeling_budget,
               'number_of_labeled_cells': len(labeled_cells), 'detected_errors_keys': detected_errors}
    result_file_path = os.path.join(results_path, f'''raha_{dataset_name}_number#{execution_number}_${labeling_budget}$labels.json''')
    act_errors_dirs = os.path.join(results_path, "act_errors")
    if not os.path.exists(act_errors_dirs):
        os.makedirs(act_errors_dirs)
    act_errors_path = os.path.join(act_errors_dirs, f'''raha_{dataset_name}_number#{execution_number}_${labeling_budget}$labels_act_errors.pickle''')
    with open(result_file_path, "w") as result_file:
        json.dump(results, result_file)
    with open(act_errors_path, 'wb') as act:
        pickle.dump(actuall_errors_dict, act)
    print("Raha's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, metrics["ed_p"], metrics["ed_r"], metrics["ed_f"]))
