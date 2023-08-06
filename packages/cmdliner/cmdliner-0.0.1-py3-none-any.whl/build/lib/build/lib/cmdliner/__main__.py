"""
  A general utility script for testing the cmdliner python library.

  Provides commands that can be used for testing.
"""
from cmdliner import Command, Application


class GreetCommand(Command):
    """
    Greets someone

    greet
        name=John : Who do you want to greet?
        --yell : Yell the name in CAPS ?
        --times=10 : number of times to repeat
    """

    def handle(self, name, yell):
        if name:
            text = 'Hello {}'.format(name)
        else:
            text = 'Hello'

        if yell:
            text = text.upper()

        print(text)


app = Application("cmdliner", "0.0", __doc__)
app.add(GreetCommand)
app.run()
