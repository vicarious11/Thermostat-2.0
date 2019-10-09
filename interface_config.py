import copy
from collections import abc
import json


class ConfigInterface:
    def __init__(self,
                 appConfig="./actuatorRecipe.json",
                 driver="./driver.json"):
        if isinstance(appConfig, abc.Mapping):
            self.frontendConfig = appConfig
        else:
            self.frontendConfig = self.read_json_file(appConfig)
        if isinstance(driver, abc.Mapping):
            self.controlsDriver = driver
        else:
            self.controlsDriver = self.read_json_file(appConfig)
        self.appMode = self.frontendConfig["recipeInfo"]["appSettings"][
            "appMode"]
        self.appSettings = self.parse_app_settings()
        self.actionSettings = self.parse_action_settings()
        self.expressions = self.parse_expressions()
        self.actionName = self.frontendConfig["recipeInfo"]["actionAlert"][0][
            "name"]

    def parse_app_settings(self):
        appSettings = {}
        appSettings["appType"] = self.frontendConfig["recipeInfo"]["appType"]
        for key, value in self.frontendConfig["recipeInfo"]["appSettings"]:
            appSettings[key] = value
        return appSettings

    def parse_action_settings(self):
        return self.frontendConfig["recipeInfo"]["actionAlert"][0]

    def parse_expressions(self):
        expressions = copy.deepcopy(self.driver[self.appMode])
        del expressions["controls"]
        expressions["%torealvalue"] = self.driver[self.appMode]["controls"][
            self.actionName]["%torealvalue"]
        return expressions

    def read_json_file(cls, filePath):
        with open(filePath) as f:
            data = json.load(f)
        return data

    def get_curves(self, controlName):
        return self.driver[self.appMode]["controls"][self.actionName]["curves"]

    def get_observation(self):
        return self.frontendConfig["observe"]

    def get_all_control_settings(self):
        controlSettings = {}
        app = self.frontendConfig["appMode"]
        for name, meta in self.frontendConfig["controls"].items():
            controlSettings[name] = {"controlParamInfo": {}, "meta": {}}
            controlSettings[name]["controlParamInfo"]["name"] = name
            controlSettings[name]["controlParamInfo"]["deviceid"] = meta[
                "deviceid"]
            controlSettings[name]["controlParamInfo"]["param"] = meta["param"]
            controlSettings[name]["meta"]["emergencyPosition"] = meta[
                "emergencyPosition"]
            controlSettings[name]["meta"]["minimumPosition"] = meta[
                "minimumPosition"]
            controlSettings[name]["meta"]["minModulation"] = meta[
                "minModulation"]
            controlSettings[name]["meta"]["maxModulation"] = meta[
                "maxModulation"]
            controlSettings[name]["meta"]["modulationSpeed"] = meta[
                "modulationSpeed"]
            controlSettings[name]["meta"]["sampleTime"] = meta["sampleTime"]
            controlSettings[name]["meta"][
                "%torealvalue"] = self.controlsDriver[app]["controls"][name][
                    "%torealvalue"]
        return controlSettings

    def get_all_app_settings(self):
        appSettings = {}
        app = self.frontendConfig["appMode"]
        if app == "cooling":
            controllerDirection = 1
        elif app == "heating":
            controllerDirection = -1

        appSettings["controllerDirection"] = controllerDirection
        appSettings["timeToAchieveSetpoint"] = self.frontendConfig[
            "timeToAchieve"]
        appSettings["degreeOfFreedom"] = self.controlsDriver["dof"]
        appSettings["setpoint"] = None
        appSettings["offset"] = None
        appSettings["maxOffset"] = self.frontendConfig["maxOffset"]
        appSettings["minOffset"] = self.frontendConfig["minOffset"]
        appSettings["cycleStartExpression"] = self.controlsDriver[app][
            "cycleStartExpr"]
        appSettings["cycleEndExpression"] = self.controlsDriver[app][
            "cycleEndExpr"]
        appSettings["minSampleTime"] = self.frontendConfig["minSampleTime"]
        appSettings["newOffsetExpression"] = self.controlsDriver[app][
            "newOffsetExpr"]
        return appSettings
