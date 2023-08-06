import sys
COLORS = {
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
}
END_COLOR = '\033[0m'


def cprint(*args, sep=' ', end='\n', file=None, color=None):
    file = file or sys.stdout
    if color is not None and color in COLORS:
        args = list(args)
        args.insert(0, COLORS[color])
        args.append(END_COLOR)
    print(*args, file=file, sep=sep, end=end)


def yes_no_prompt(message, tries=10, default='n', color=None, trailing=': '):
    return prompt(message, choices=['y', 'n'], default=default, color=color, trailing=trailing, tries=tries).lower()\
           == 'y'


def prompt(message, match=None, match_function=None, choices=None, tries=10, default=None, allow_empty=False,
           color=None, trailing=': ', case_sensitive=False, description=None):
    t = 0
    prompt_message = message
    default_showed = default is None

    # choices
    if not case_sensitive and choices is not None:
        choices = [c.lower() for c in choices]
    if choices is not None:
        if default is not None and default in choices and not case_sensitive:
            prompt_message += ' [%s]' % '/'.join([c if c != default else c.upper() for c in choices])
            default_showed = True
        else:
            prompt_message += ' [%s]' % '/'.join(choices)
    # description & default value
    if description is not None:
        prompt_message += ' (%s)' % description
    elif not default_showed:
        prompt_message += ' (Default: %s)' % default

    # trailing
    prompt_message += trailing
    if not case_sensitive and choices is not None:
        choices = [c.lower() for c in choices]
    if color is not None and color in COLORS:
        prompt_message = COLORS[color] + prompt_message + END_COLOR
    while t < tries:
        data = input(prompt_message)
        datac = data if case_sensitive else data.lower()

        if len(data.strip()) == 0 and default is not None:
            return default
        if choices is not None:
            if datac in choices:
                return data
        elif match is not None:
            if match.match(datac):
                return data
        elif match_function is not None:
            if match_function(datac):
                return data
        else:
            if allow_empty or len(data.strip()) > 0:
                return data
        t += 1
    raise ValueError("Max tries reached! data entered by the user is not valid!")


