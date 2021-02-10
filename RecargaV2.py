import yaml

def config():
    with open ("Sitios.yml", mode='r') as file:
        _config=yaml.safe_load(file)
    return _config