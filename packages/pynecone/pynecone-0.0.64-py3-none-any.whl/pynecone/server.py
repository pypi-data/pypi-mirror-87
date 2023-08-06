from pynecone import Shell

class Server(Shell):

        def __init__(self):
            super().__init__('server')

        def get_commands(self):
            return [
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'Server shell'