import win32api
import win32print
import os

class Printer:

    def __init__(self):
        self.pHandle = win32print.GetDefaultPrinter()
        self.BASE_DIR = os.getcwd() 

    def printBill(self):
        win32api.ShellExecute (
                                0,
                                "print",
                                 os.path.join(self.BASE_DIR, 'source', 'lastBill.txt'),
                                #
                                # If this is None, the default printer will
                                # be used anyway.
                                #
                                '/d:"%s"' % self.pHandle,
                                ".",
                                0
                                )
        
    def printSummary(self):
        win32api.ShellExecute (
                                0,
                                "print",
                                 os.path.join(self.BASE_DIR, 'source', 'totalBill.txt'),
                                #
                                # If this is None, the default printer will
                                # be used anyway.
                                #
                                '/d:"%s"' % self.pHandle,
                                ".",
                                0
                                )
        
    def openCashDrawer(self):
        win32api.ShellExecute (
                                0,
                                "print",
                                 os.path.join(self.BASE_DIR, 'source', 'empty.txt'),
                                #
                                # If this is None, the default printer will
                                # be used anyway.
                                #
                                '/d:"%s"' % self.pHandle,
                                ".",
                                0
                                )