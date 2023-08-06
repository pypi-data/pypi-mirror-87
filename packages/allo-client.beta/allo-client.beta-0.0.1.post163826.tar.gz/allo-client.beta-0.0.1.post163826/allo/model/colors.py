# -*- coding: utf-8 -*-


class BColors:
    HEADERD = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNINGD = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def __handle(message, color, log):
        tolog = color + message + BColors.ENDC
        if log:
            print(tolog)
        else:
            return tolog

    @staticmethod
    def success(message, log=True):
        return BColors.__handle(message, BColors.OKGREEN + BColors.BOLD, log)

    @staticmethod
    def info(message, log=True):
        return BColors.__handle(message, BColors.OKBLUE, log)

    @staticmethod
    def error(message, log=True):
        return BColors.__handle(message, BColors.FAIL + BColors.BOLD, log)

    @staticmethod
    def header(message, log=True):
        return BColors.__handle(message, BColors.HEADERD, log)

    @staticmethod
    def warning(message, log=True):
        return BColors.__handle(message, BColors.WARNINGD, log)
