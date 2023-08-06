from colorama import init
import datetime

init()

class Log:
    """docstring for logger."""

    def __init__(self, Shell=True,File=None):
        self.shell = Shell
        self.file = file

    def info(self,logoutput):
        if self.shell == True:
            print(u"\u001b[36m[INFO]\u001b[0m" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)
        else:
            with open(self.file,"a") as f:
                print("[INFO]:" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)

    def error(self,logoutput):
        if self.shell == True:
            print(u"\u001b[31m[ERROR]\u001b[0m" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)
        else:
            with open(self.file,"a") as f:
                print("[ERROR]:" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)

    def warning(self,logoutput):
        if self.shell == True:
            print(u"\u001b[33m[WARNING]\u001b[0m" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)
        else:
            with open(self.file,"a") as f:
                print("[WARNING]:" +  datetime.now().strftime('%M:%S.%f')[:-4] + ":" + logoutput)
