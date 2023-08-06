class Status:
    # dictionary of action states
    ACTION_STATES = {
        -1: 'ERROR',
        0: 'CONFIGURED',
        1: 'PENDING',
        2: 'EXECUTING',
        3: 'COMPLETE',
    }

    def __init__(self):
        """Mixin for reporting status states and strings"""
        pass

    @property
    def status_code(self) -> int:
        """returns a status code representative of the state of the Action"""
        return 0

    @property
    def status_string(self) -> str:
        """string meaning of status code"""
        return self.ACTION_STATES[self.status_code]

    @property
    def status(self) -> str:
        """status string for the Action"""
        return f'{self.status_code}: {self.status_string}'
