import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetVideoFormatResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        self.videoFormat = result["format"]

        ResultBase.__init__(self, self.videoFormat >= 0, successMessage, failMessage)
