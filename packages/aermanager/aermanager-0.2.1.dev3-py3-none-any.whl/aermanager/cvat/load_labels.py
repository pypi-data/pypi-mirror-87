import json
import os


def load_labels_as_dict(file_path: str):
    assert os.path.exists(file_path), "The specified path doesn't exist!"

    with open(file_path) as json_file:
        labels = json.load(json_file)

        labels_list = ['__Empty_Default__'] + [label['name'] for label in labels]

        dict_iterator = zip(labels_list, range(0, len(labels_list)))

        return dict(dict_iterator)