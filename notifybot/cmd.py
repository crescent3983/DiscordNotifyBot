from cmd import Cmd
import sys

class CommandLine(Cmd):

    def do_quit(self, args):
        print("Quitting.")
        sys.exit()
