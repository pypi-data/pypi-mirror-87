# cmdliner

The usage was inspired on [Cleo](https://github.com/sdispater/cleo) .


```python
from cmdliner import Command


class GreetCommand(Command):
    """
    Greets someone

    greet
        {name?'' : Who do you want to greet?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self, name, yell):
        if name:
            text = 'Hello {}'.format(name)
        else:
            text = 'Hello'

        if yell:
            text = text.upper()

        print(text)
```