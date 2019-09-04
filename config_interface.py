import json


class ConfigError(Exception):
    pass


class ConfigInterface:

    thermalControlsInfoPath = "./controls.json"
    thermalFrontendConfigFilePath = "./config_from_frontend.json"

    def __init__(self):
        try:
            with open(self.thermalFrontendConfigFilePath) as f:
                self.configFromFrontend = json.load(f)
            with open(self.thermalControlsInfoPath) as f:
                self.controlsSetting = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            raise ConfigError

    def get_curves(self, controlName):
        return self.controlsSetting[controlName]["curves"]

    def get_observation(self, controlName):
        return self.configFromFrontend["controls"][controlName][
            "observableformula"]
