import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Params:
    _instance = None

    def __new__(cls, config_file: str) -> 'Params':
        if cls._instance is None:
            cls._instance = super(Params, cls).__new__(cls)
            with open(config_file, "r") as f:
                print("Loading YAML")
                config = yaml.safe_load(f)
            cls._instance._load_params(config)
        return cls._instance

    def _load_params(self, config: dict) -> None:
        self.HEADLESS = config["webdriver"]["headless"]
        self.NO_SANDBOX = config["webdriver"]["no_sandbox"]
        self.TIMEOUT = config["webdriver"]["timeout"]

        self.URL = config["crawler"]["url"]
        self.DEMARCACIONES = config["crawler"]["demarcaciones"]
        self.VIAS = config["crawler"]["vias"]
        self.OBRAS = config["crawler"]["obras"]
        
        self.INTERVALO = config["app"]["interval"]

def get_params(config_file: str) -> Params:
    return Params(config_file)

# # Example usage:
# params = Params()
# print(params.HEADLESS)
# print(params.DEMARCACIONES)