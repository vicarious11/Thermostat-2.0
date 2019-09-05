import json


class ConfigInterface:
    def __init__(self,
                 thermostatFrontendConfig="./config_from_frontend.json",
                 thermostatControlsDriver="./controls.json"):
        self.frontendConfig = self.read_json_file(thermostatFrontendConfig)
        self.controlsDriver = self.read_json_file(thermostatControlsDriver)

    def read_json_file(cls, filePath):
        with open(filePath) as f:
            data = json.load(f)
        return data

    def get_curves(self, controlName):
        return self.controlsDriver[controlName]["curves"]

    def get_observation(self, controlName):
        return self.frontendConfig["controls"]["observableformula"]
