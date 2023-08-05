import sys
import json

from testwizard.commands_core import CommandBase
from .GetVideoFormatResult import GetVideoFormatResult


class GetVideoFormatCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "GetVideoFormat")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetVideoFormatResult(result, "GetVideoFormat was successful", "GetVideoFormat failed")
