import os
import yaml


def load_yaml(filepath: str) -> dict:
    """Loads a yaml file.

    Can be used as stand alone script by

    :params filepath: file path to the yaml file to be loaded.

    :usage:

       `load_yaml.py --filepath /file/path/to/filename.yaml`

    :return: a dictionary object
    """

    assert os.path.isfile(filepath)

    if not os.path.isfile(filepath):
        print(f"`filepath` missing = `{filepath}`, ensure `filepath` exist or "
              "if standalone `--filepath /file/path/filename.yaml` argument is given.")
        return None
    else:
        with open(filepath, 'r') as file_descriptor:
            try:
                yaml_data = yaml.safe_load(file_descriptor)
            except Exception as msg:
                print(f'File `{filepath}` loading error. \n {msg}')
            else:
                return yaml_data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--filepath', action="store",
                        dest="filepath", type=str, default=True)
    args = parser.parse_args()
    load_yaml(args.filepath)
