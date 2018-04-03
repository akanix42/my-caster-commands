from dragonfly import (Grammar, RuleRef, RuleWrap, Dictation, Key, Text, Function,
                       Alternative, AppContext, Compound)

from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

import myRules._dragonfly_utils as utils
from myRules.actionWebApi.send_command import send_command, IdeaAction

# class TypeRule(Compound):
#   spec = '<type> [or]'
#   extras = [
#       Choice(
#         name = 'type',
#         choices = {
#           'string': 'string',
#           'number': 'number',
#           'object': 'object',
#           'boolean': 'boolean',
#           'void': 'void',
#           'null': 'null',
#           'undefined': 'undefined',
#           'any': 'any',
#           'Date': 'Date',
#         }),
#   ]
#
#
# class TypesRule(Compound):
#   spec = '<types>'
#   extras = [
#     Repetition(
#       name = 'types',
#       child = TypeRule,
#       max = 8)
#   ]
#
#   def _process_recognition(self, node, extras):
#     print ('types', extras['types'])
#     types = extras['types']
#     extras['types'] = ' | '.join(types)
#
#
# class FunctionParamRule(Compound):
#   spec = 'par <param> [types]'
#   extras = [
#     Dictation('param'),
#     TypesRule('types'),
#
#   ]
from myRules.rules.webstorm.ide import F
from myRules.sharedMappings.dictation import dictation_element
from myRules.utilities import text_format


def format_code():
    send_command('Reformat_code')


def write_function(name):
    template = 'function {name}() {{'  # no ending bracket necessary, WebStorm automatically adds it
    Text(template.format(name = name)).execute()
    Key('enter').execute()
    format_code()
    Key('a-up,end,left:3').execute()


def writeParam(name):
    Text('{name},'.format(name = name)).execute()
    format_code()


def deleteBlock():
    send_command('CollapseRegion')
    send_command('EditorDeleteLine')
    # Key('c-minus,c-y').execute()


def findText(text):
    Key('c-f/25').execute()
    Text(text).execute()


#
# formatted_dictation = utils.create_rule(
#     'FormatRule',
#     {
#         'camel <dictation>': Function(textFormat.format_camel),
#     },
#     {'dictation': Dictation()}
# )
#
# dictation_rule = utils.create_rule(
#     'DictationRule',
#     {
#         '<text>': Text('%(text)s'),
#     },
#     {
#         'text': Dictation()
#     }
# )
# dictation_element = RuleWrap(None, Alternative([
#     RuleRef(rule=dictation_rule),
# ]))


# def FuncWrap(node, extras):
#     return echo(extras.name)
#
#
def echo(dictation):
    return '{dictation}'.format(dictation = dictation)


#
#
# def FuncWrap1(node, extras):
#     return echo2(**extras)


def newJsFile(name):
    send_command('NewJavaScriptFile')
    Text('{name}'.format(name = name)).execute()
    Key('enter').execute()


def callFunction(dictation):
    return


class WebStormFunctionRules(MergeRule):
    pronunciation = 'web storm custom'

    mapping = {
        'function [<dictation>]': R(Function(write_function), rdescript = 'WebStorm: Generate Function'),
        'par <dictation>': R(Function(writeParam), rdescript = 'WebStorm: Write Function Param'),
        'arg <dictation>': R(Function(writeParam), rdescript = 'WebStorm: Write Function Arg'),
        'type <dictation>': R(Function(writeParam), rdescript = 'WebStorm: Write Type'),
        'params':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToFunctionParameters')),
        'previous function':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToPreviousFunctionName')),
        'next function':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToNextFunctionName')),
        'current function':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToFunctionName')),
        'previous argument':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToPreviousArgument')),
        'next argument':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToNextArgument')),
        'previous parameter':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToPreviousParameter')),
        'next parameter':
            R(IdeaAction('com.nathantreid.codeNavigationHelpers.Actions.MoveCaretToNextParameter')),
        # 'go to arrow params': R(Function(findText, text = 'params')),
        'new javascript file [<dictation>]': R(Function(newJsFile)),
        'call <dictation>': Function(write_function),
    }
    extras = [
        Alternative(
            name = 'dictation',
            children = [
                dictation_element,
                Compound(spec = '<dictation>', value_func = F(text_format.format_camel), extras = [
                    Dictation('dictation')
                ])
            ],
        ),
    ]
    defaults = {'n': 1, }


# navigate to function parameters from inside function:
# alt + up
# end
# left (3)


context = AppContext(executable = 'WebStorm', title = 'WebStorm') \
          | AppContext(executable = 'WebStorm64', title = 'WebStorm') \
          | AppContext(executable = 'java', title = 'WebStorm')

grammar = Grammar('WebStorm Function', context = context)
rule = WebStormFunctionRules(name = 'web storm function')
gfilter.run_on(rule)
grammar.add_rule(rule)
grammar.load()
