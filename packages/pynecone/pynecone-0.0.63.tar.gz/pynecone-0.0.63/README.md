# pynecone

A library to make writing cli applications easier

    Usage example:
    
        from pynecone import Shell, Cmd
    
    
    class MyCmd1(Cmd):
    
        def __init__(self):
            super().__init__("mycommand1")
    
        def add_arguments(self, parser):
            parser.add_argument('--foo1', help='foo help')
    
        def run(self, args):
            print("*** hello from mycommand1, foo1 is {0}".format(args.foo1))
    
        def get_commands(self):
            return [self]
    
        def get_help(self):
            return 'mycommand1 help'
    
    class MyCmd2(Cmd):
    
        def __init__(self):
            super().__init__("mycommand2")
    
        def add_arguments(self, parser):
            parser.add_argument('--foo2', help='foo help')
    
        def run(self, args):
            print("*** hello from mycommand2, foo2 is {0}".format(args.foo2))
    
        def get_commands(self):
            return [self]
    
        def get_help(self):
            return 'mycommand2 help'
    
    
    class MySubshell1(Shell):
    
        def get_help(self):
            return "mysubshell1 help"
    
        def __init__(self):
            super().__init__("mysubshell1")
    
        def get_commands(self):
            return [MyCmd1(), MyCmd2()]
    
        def add_arguments(self, parser):
            parser.add_argument('--bar1', help='bar1 help')
    
    class MySubshell2(Shell):
    
        def get_help(self):
            return "mysubshell2 help"
    
        def __init__(self):
            super().__init__("mysubshell2")
    
        def get_commands(self):
            return [MyCmd1(), MyCmd2()]
    
        def add_arguments(self, parser):
            parser.add_argument('--bar2', help='bar2 help')
    
    
    # python tests/demo.py --oof 123 mycommand1 --foo1 456
    class MyShell(Shell):
    
        def get_help(self):
            return "you can run mycommand1 or mycommand2 commands"
    
        def __init__(self):
            super().__init__('myshell')
    
        def get_commands(self):
            return [MyCmd1(), MyCmd2()]
    
        def add_arguments(self, parser):
            parser.add_argument('--oof', help='oof help')
    
    # python tests/demo.py mysubshell2 --bar2 456  mycommand2 --foo2 123
    class MyShell2(Shell):
    
        def get_help(self):
            return "you can run mysubshell1 or mysubshell2 subshells"
    
        def __init__(self):
            super().__init__('myshell2')
    
        def get_commands(self):
            return [MySubshell1(), MySubshell2()]
    
        def add_arguments(self, parser):
            parser.add_argument('--oof', help='oof help')
    
    def main():
        #MyShell().run()
        MyShell2().run()
    
    
    if __name__ == "__main__":
        main()