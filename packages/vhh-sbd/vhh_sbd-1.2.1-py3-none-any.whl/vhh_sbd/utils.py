import sys


class STDOUT_TYPE:
    """
    This class represents message types.
    """
    INFO = 1
    ERROR = 2


def printCustom(msg: str, type: int):
    """
    This function represents a customized print function (error/info msg).
    :param msg: Message to print.
    :param type: Type of message (info or error).
    """
    if(type == 1):
        print("INFO: " + msg)
    elif(type == 2):
        print("ERROR: " + msg)
    else:
        print("FATAL ERROR: stdout type does not exist!")
        exit()




def getCommandLineParams():
    """
    This function is used to read commandline parameters (e.g. just used in development stage)
    :return: list of parameters.
    """
    printCustom("read commandline arguments ... ", STDOUT_TYPE.INFO)
    number_of_args = len(sys.argv)
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    if (number_of_args < 3):
        printCustom("There must be at least two commandline argument(s)", STDOUT_TYPE.ERROR)
        exit()

    params = sys.argv
    print(params)
    return params

