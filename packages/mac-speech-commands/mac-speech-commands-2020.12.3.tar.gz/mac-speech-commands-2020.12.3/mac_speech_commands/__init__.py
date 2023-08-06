__all__ = ['replace']


import re

"""
https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/FineTuning/FineTuning.html
"""


def replace(text, functions):
    """replace speech commands in text with functions output"""
    def repl(m):
        command = m[0][2:-2].split(" ")[0]
        value = " ".join(m[0][2:-2].split(" ")[1:])
        if command in functions:
            func = functions[command]
            return func(value)
        return m[0]
    return re.sub(r'\[\[(.+)\]\]', repl, text)
