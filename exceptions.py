class Impossible(Exception):
    """Exception raised when an action is impossible to be performed.

    The reason is given as the exception message.
    """


class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatically saving."""


class StartNewGame(Exception):
    """Start a new game."""


class SaveAndQuitToMainMenu(Exception):
    """Save and quit to main menu."""
