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
            self.controlsDriver = self.read_json_file(driver)
        self.appMode = self.frontendConfig["recipeInfo"]["appSettings"][
            "appMode"]
        self.appSettings = self.parse_app_settings()
        self.actionSettings = self.parse_action_settings()
        self.actionName = self.frontendConfig["recipeInfo"]["actionAlert"][0][
            "name"]
        self.expressions = self.parse_expressions()

    def parse_app_settings(self):
        appSettings = {}
        appSettings["appType"] = self.frontendConfig["recipeInfo"]["appType"]
        for key, value in self.frontendConfig["recipeInfo"][
                "appSettings"].items():
            appSettings[key] = value
        return appSettings

    def parse_action_settings(self):
        return self.frontendConfig["recipeInfo"]["actionAlert"][0]

    def parse_expressions(self):
        expressions = copy.deepcopy(self.controlsDriver[self.appMode])
        del expressions["controls"]
        expressions["%torealvalue"] = self.controlsDriver[
            self.appMode]["controls"][self.actionName]["%torealvalue"]
        return expressions

    def read_json_file(cls, filePath):
        with open(filePath) as f:
            data = json.load(f)
        return data

    def get_curves(self, controlName):
        return self.controlsDriver[self.appMode]["controls"][
            self.actionName]["curves"]
