import json
import os

from platform import system

from platformio.managers.platform import PlatformBase
from platformio.util import get_systype

class HWLogic(PlatformBase):

    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        board_config = self.board_config(board)
        build_core = variables.get(
            "board_build.core", board_config.get("build.core", "arduino"))

        frameworks = variables.get("pioframework", [])
        if "arduino" in frameworks:
            self.packages["toolchain-gccarmnoneeabi"]["version"] = "~1.90201.0"
            self.packages["framework-cmsis"]["version"] = "~2.50501.0"
            self.packages["framework-cmsis"]["optional"] = False

        if any(f in frameworks for f in ("cmsis", "stm32cube")):
            self.packages["tool-ldscripts-ststm32"]["optional"] = False

        default_protocol = board_config.get("upload.protocol") or ""
        if variables.get("upload_protocol", default_protocol) == "dfu":
            self.packages["tool-dfuutil"]["optional"] = False


        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result
