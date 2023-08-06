import yaml


def load_config(path):
    return yaml.load(open(path, 'r'), yaml.Loader)
