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
        return self.controlsDriver["controls"][controlName]["curves"]

    def get_observation(self, controlName):
        return self.frontendConfig["controls"]["observableformula"]

    def get_all_control_settings(self):
        controlSettings = {}
        for name, meta in self.frontendConfig["controls"].items():
            controlSettings[name] = {"controlParamInfo": {}, "meta": {}}
            controlSettings[name]["controlParamInfo"]["name"] = name
            controlSettings[name]["controlParamInfo"]["deviceid"] = meta[
                "deviceid"]
            controlSettings[name]["controlParamInfo"]["param"] = meta["param"]
            controlSettings[name]["meta"]["emergencyPosition"] = meta[
                "emergencyPosition"]
            controlSettings[name]["meta"]["minModulation"] = meta[
                "minModulation"]
            controlSettings[name]["meta"]["maxModulation"] = meta[
                "maxModulation"]
            controlSettings[name]["meta"]["modulationSpeed"] = meta[
                "modulationSpeed"]
            controlSettings[name]["meta"]["sampleTime"] = meta["sampleTime"]
        return controlSettings

    def get_all_app_settings(self):
        appSettings = {}

        if self.frontendConfig["appMode"] == "cooling":
            controllerDirection = 1
        elif self.frontendConfig["appMode"] == "heating":
            controllerDirection = -1

        appSettings["controllerDirection"] = controllerDirection
        appSettings["timeToAchieveSetpoint"] = self.frontendConfig[
            "timeToAchieve"]
        appSettings["degreeOfFreedom"] = self.controlsDriver["dof"]
        appSettings["setpoint"] = None
        appSettings["offset"] = None
        return appSettings
