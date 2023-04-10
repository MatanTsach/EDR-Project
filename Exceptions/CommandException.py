class CommandException(Exception):
    '''Exception raised for errors in the command input.'''

    def __init__(self, message):
        self.message = message
        super().__init__(f'Command Error: {self.message}')

    def __str__(self):
        return self.message