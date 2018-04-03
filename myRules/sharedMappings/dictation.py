from dragonfly import Dictation

from myRules.actions.func_choice import FuncChoice, F
from myRules.utilities import text_format, echo

dictation_element = FuncChoice(choices = {
    "echo <dictation>": F(echo.echo),
    "camel <dictation>": F(text_format.format_camel),
    "pascal <dictation>": F(text_format.format_pascal),
    "snake <dictation>": F(text_format.format_score),
    "kebab <dictation>": F(text_format.format_dashes),
    "one word <dictation>": F(text_format.format_one_word),
    "upper one word <dictation>": F(text_format.format_upper_one_word),
    "spaces <dictation>": F(text_format.format_spaces),
    "upper spaces <dictation>": F(text_format.format_upper),
}, extras = [
    Dictation("dictation"),
])
