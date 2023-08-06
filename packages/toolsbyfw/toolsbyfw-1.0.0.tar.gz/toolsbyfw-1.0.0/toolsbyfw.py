import sys
import os

class tools:
    def __init__(self):
        pass

    def commands():
        print('tools.exit() - Exit for you programm')
        print('tools.run() - Run command for you system console example: tools.run(command = "echo Hello World!")')
        print('tools.checkdir() - Check you programm directory')

    def exit():
        sys.exit(1)

    def run(command):
        os.system( command )

    def checkdir():
        diros = os.getcwd()
        print(f'{ diros }')

