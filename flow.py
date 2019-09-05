from control import Control
from interface_config import ConfigInterface
from interface_transport import TransportInterface


class ApplicationFlow:
    def __init__(self, interface, appSettings):
        self.interface = interface
        self.configInterface = interface["config"]
        self.transportInterface = interface["transport"]
        self.appSettings = appSettings
        self.controlSettings = self.configInterface.get_all_control_settings()
        self.controls = [
            Control(self.interface, controlSetting["controlParamInfo"],
                    controlSetting["meta"], self.appSettings)
            for _, controlSetting in self.controlSettings.items()
        ]


def main():
    configInterface = ConfigInterface()
    transportInterface = TransportInterface()
    interface = {"config": configInterface, "transport": transportInterface}
    appSettings = configInterface.get_all_app_settings()
    flow = ApplicationFlow(interface, appSettings)
    return flow
