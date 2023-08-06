import logging
from abc import ABC, abstractmethod


class MessagerBase(ABC):

    def __init__(self):
        self._logger =  None
    @property
    def logger(self):
        if self._logger is None:
            self._logger = logging.getLogger("assetic")

            if self._logger is None:
                self._logger = logging.getLogger(__file__)

        return self._logger

    @abstractmethod
    def new_message(self, msg, *args):
        pass
