
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape
import io
from lark import Lark, Transformer


####################################
## GLOBAL CONSTANTS 
####################################

# Dirty but needed : all the fields required to create a question
# We also set their default value, and an alias when the fields has a weird/toolong name
DICT_DEFAULT_QUESTION_MOODLE = { 
    # general stuff
    '@type': {'default': "essay", 
              'alias': 'type'
             }, # can be "multichoice" for MCQs
    "name": {'default': "Default question title", 
             'attribute': {'@format': 'txt'}, 
             'alias': 'title'
            },
    "questiontext": {'default': "Default question text", 
                     'attribute': {'@format': 'html'}, 
                     'alias': 'text'
                    },
    "generalfeedback": {'default': "", 'attribute': {'@format': 'html'}},
    "defaultgrade": {'default': 1.0, 
                     'alias': 'grade'
                    },
    "penalty": {'default': 0.0},
    "hidden": {'default': 0},
    "idnumber": {'default': ""},
    # 'essay' specifics
    "responseformat": {'default': "editorfilepicker"}, # by default allow to upload a file as answer. Set "editor" ottherwise
    "responserequired": {'default': 0}, # 0 for no response required, 1 for yes
    "responsefieldlines": {'default': 10},
    "attachments": {'default': -1}, # number of attachments allowed. -1 is infinty
    "attachmentsrequired": {'default': 0}, # 0 for no attachment required, 1 for yes
    "graderinfo": {'default': "", # correction for the grader
                   'attribute': {'@format': 'html'}, 
                   'alias': 'infocorrecteur'
                  }, 
    "responsetemplate": {'default': "", 'attribute': {'@format': 'html'}},
    # 'multichoice' specifics
    "single" : {'default': "true"}, # Says if only a unique answer is possible
    "shuffleanswers" : {'default': "true"}, # Constantly shuffles the possible choices
    "answernumbering" : {'default': "none"}, # Other choices : 'abc', '123', 'iii', and certainly caps
    "correctfeedback": {'default': "Votre réponse est correcte.", 'attribute': {'@format': 'html'}},
    "partiallycorrectfeedback": {'default': "Votre réponse est partiellement correcte.", 'attribute': {'@format': 'html'}},
    "incorrectfeedback": {'default': "Votre réponse est incorrecte.", 'attribute': {'@format': 'html'}},
    "shownumcorrect" : {'default': ""}, # No idea
    "answer" : {'default': "", 'list': []} # We deal with this in the Answer class
}

def dict_default_question_moodle():
    return DICT_DEFAULT_QUESTION_MOODLE


# to deal with mess between Latex, python and xml special characters
# \u and \x not supported but useless for inline latex?
UNESCAPE_LATEX = { 
    '\x07' : '\\a', 
    '\x0c' : '\\f', 
    '\x0b' : '\\v', 
    '\x08' : '\\b', 
    '\n'   : '\\n', 
    '\r'   : '\\r', 
    '\t'   : '\\t' 
} 


####################################
## STRING FUNCTIONS
####################################

def alias(field): # easy access to alias
    if 'alias' in dict_default_question_moodle()[field]:
        return dict_default_question_moodle()[field]['alias']
    else:
        return field

def isfield(string):
    for key in dict_default_question_moodle().keys():
        if string in [key, alias(key)]:
            return True
    return False

def cleanstr(string, raw=False):
    if raw:
        string = string.replace('\t','') # no tabs
        string = string.replace('\n','') # no linebreak BEWARE this might destroy protected string
    else:
        string = string.replace('\t','  ') # double space instead of tabs
    return string

def savestr(string, filename="new.txt", raw=False):
    string = cleanstr(string, raw)
    text_file = io.open(filename, "w", encoding='utf8') # essential for accents and other characters
    text_file.write(string)
    text_file.close()

def latex_protect(string):
    return unescape(string, UNESCAPE_LATEX)
    
def html(string):
    if string is "":
        return string
    else:
        return "<![CDATA[<p>\(\)" + tex_parse_dollar(latex_protect(string)) + "</p>]]>"  # \(\) is a hack to activate latex dans Moodle. Not always needed, not always working. Still a mystery to me.

def set_oparg(variable, default_value): #optional argument manager
    if variable is None:
        return default_value
    else:
        return variable
    
def printmk(*tuple_of_text):
    from IPython.display import display, Markdown
    L = [Markdown(text) for text in tuple_of_text]
    return display(*tuple(L))






def replace_open_close(string, old, newopen, newclose):
    # Given a string containing PAIRS of 'old' chains of characters
    # replace 'old' with opening/closing chains of characters
    oldsize = len(old)
    target_idx = [idx for idx in range(len(string)) if string[idx:idx+oldsize] == old]
    if len(target_idx) % 2 == 0:
        target_open_idx = target_idx[0::2]
        target_close_idx = target_idx[1::2]
        diff = 0 # controls the difference in size bewtween old and new strings
        gap_open = len(newopen) - oldsize
        for idx in target_open_idx:
            string = string[:idx+diff] + newopen + string[idx+oldsize+diff:]
            diff = gap_open + diff
        diff = gap_open # we reset but not to zero since there is an already replaced "open" character before the first "close" one
        gap_close = len(newclose) - oldsize + gap_open # every time we move forward we accumulate a shit from both "open" and "close" characters
        for idx in target_close_idx:
            string = string[:idx+diff] + newclose + string[idx+oldsize+diff:]
            diff = gap_close + diff
    else:
        raise ValueError("I have to replace '"+old+"' with *pairs* of characters but I see "+str(len(target_idx))+" of them which is an odd number")
    return string

def tex_parse_dollar(latex):
    # Transform a string containing latex expressions to make it compatible with most
    # web-based applications which prefer \(...\) or \[...\] syntax.
    latex = replace_open_close(latex, '$$', '\\[', '\\]')
    latex = replace_open_close(latex, '$', '\\(', '\\)')
    return latex


"""
This was INDECENTLY SLOW. Like 1 full second to convert an empty string?????
I couldn't make any parser to work properly. In the end I hard coded it myself.
It is quite fast now (10000 calls/second), and more robust (allows for newlines etc).

# Taken from https://gist.github.com/erezsh/1f834f7d203cb1ac89b5b3aa877fa634


class T(Transformer):
    def mathmode_offset(self, children):
        return '\\[' + ''.join(children[1:-1]) + '\\]'

    def mathmode_inline(self, children):
        return '\\(' + ''.join(children[1:-1]) + '\\)'

    def tex(self, children):
        return ''.join(children)

def tex_parse_dollar(string):
    lark = Lark(r'''
         tex: (mathmode_offset | mathmode_inline | TEXT)+
         mathmode_offset: OFFSETDOLLAR TEXT+ OFFSETDOLLAR | OFFSETOPEN TEXT+ OFFSETCLOSE
         mathmode_inline: INLINEOPEN TEXT+ INLINECLOSE | INLINE TEXT+ INLINE
         INLINE: "$"
         INLINEOPEN: "\\("
         INLINECLOSE: "\\)"
         OFFSETDOLLAR: "$$"
         OFFSETOPEN: "\\["
         OFFSETCLOSE: "\\]"
         TEXT: /[^\]$]+/s
         ''', start='tex', parser='lalr')
    return T().transform(lark.parse(string)) # string.replace('\n', '') destroys the protected \\n, we need to be smarter here

def test_tex_parse_dollar():
    TEST_BAG = { 
        "h$e$y" : "h\(e\)y",
        "h$$e$$y" : "h\[e\]y",
        "$\begin{pmatrix} 1 \\ 2 \end{pmatrix}$" : "\(\begin{pmatrix} 1 \\ 2 \end{pmatrix}\)",
        "$f(x) = \frac{1}{x}$" : "\(f(x) = \frac{1}{x}\)"
    }
    for key in TEST_BAG:
        assert tex_parse_dollar(key) == TEST_BAG[key], key+" should return "+TEST_BAG[key]
        
"""