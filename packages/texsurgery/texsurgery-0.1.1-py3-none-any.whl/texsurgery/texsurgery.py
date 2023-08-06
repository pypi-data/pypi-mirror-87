# -*- coding: utf-8 -*-
from .simplekernel import SimpleKernel
from pyparsing import nestedExpr, Optional, Word, alphanums,\
                      originalTextFor, Literal, SkipTo, Empty, Or

def skipToMatching(opener, closer):
    """

    :param opener: opening token
    :param closer: closing token

    """
    # https://github.com/sagemath/sagetex/issues/6#issuecomment-734968972
    nest = nestedExpr(opener, closer)
    return originalTextFor(nest)

class TexSurgery(object):
    """TexSurgery allows to make some replacements in LaTeX code"""

    def __init__(self, tex_source):
        super(TexSurgery, self).__init__()
        self.original_src = tex_source
        self.src = tex_source
        #self.kernel is a lazy property
        self._kernel = self.kernel_name = None

    def __del__(self):
        """
        ## Description
        Destructor. Shuts down kernel safely.
        """
        self.shutdown()

    def shutdown(self):
        if self._kernel:
            self._kernel.kernel_manager.shutdown_kernel()
            self._kernel = None

    @property
    def kernel(self):
        if not self._kernel:
            self._kernel = SimpleKernel(self.kernel_name)
        return self._kernel

    def _add_import_action(self, packagename, options):
        def action(l,s,t):
            return '\\documentclass'+ t.restofline + '\n\\usepackage%s{%s}'%(
                '[%s]'%options if options else '',
                packagename
            )
        return action

    def add_import(self, packagename, options=''):
        documentclass = (
            '\\documentclass'+ SkipTo('\n')('restofline')
        )
        documentclass.setParseAction(
            self._add_import_action(packagename, options)
        )
        self.src = documentclass.transformString(self.src)
        return self

    def data_surgery(self, replacements):
        #TODO: use pyparsing instead of regex, for the sake of uniformity
        src = self.src
        import re
        revars = re.compile('|'.join(r'\\'+key for key in replacements))
        pos,pieces = 0, []
        m = revars.search(src)
        while m:
            start,end = m.span()
            pieces.append(src[pos:start])
            #start+1, since the backslash \ is not part of the key
            name = src[start+1:end]
            pieces.append(replacements[name])
            pos = end
            m = revars.search(src, pos=pos)
        pieces.append(src[pos:])
        self.src = ''.join(pieces)
        return self

    def latexify(self, results):
        #TODO 'image/png' grab base64 data, write to a file
        # then insert includegraphics
        #TODO do something special with 'text/html'?
        #TODO error -> texttt
        return '\n'.join(
            r.get('text/plain') or r.get('text/html') or r.get('error')
            for r in results
        )

    def runsilent(self, l, s, t):
        self.kernel.executesilent(t.content)
        return ''

    def run(self, l, s, t):
        return self.latexify(self.kernel.execute(t.content, allow_errors=True))

    def eval(self, l, s, t):
        code =  t.content[1:-1]
        return self.latexify(self.kernel.execute(code))

    def _strip_quotes(self, s):
        if isinstance(s, str) and (s[0]==s[-1]=="'" or s[0]==s[-1]=='"'):
            return s[1:-1]
        return s

    def evalstr(self, l, s, t):
        code =  t.content[1:-1]
        results = self.kernel.execute(code)
        return '\n'.join(
            self._strip_quotes(r.get('text/plain')) or r.get('text/html') or r.get('error')
            for r in results
        )

    def sage(self, l, s, t):
        code =  t.content[1:-1]
        return self.latexify(self.kernel.execute('latex(%s)'%code))

    def _truish(self, s):
        '''Return True if he string correspond to the True value
        in the current kernel'''
        if self.kernel_name in ('python2', 'python3', 'sagemath'):
            #TODO: non exhaustive (but just a helper for the user!)
            return s not in ('False', '', '[]', '0', '0.0')
        else:
            return s in ('true', 'True')

    def sif(self, l, s, t):
        code =  t.condition[0][0]
        results = self.kernel.execute(code)
        if (len(results)==1 and
            self._truish(results[0].get('text/plain'))):
            return t.texif[0][0]
        else:
            return t.texelse[0][0]

    def code_surgery(self):
        # Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        #  or whatever interactive command line application
        # Use pyparsing as in student_surgery to go through sage|sagestr|sagesilent|sif|schoose in order
        # Use SimpleKernel to comunicate with a sage process ?

        # Look for usepackage[kernel]{surgery} markup to choose the kernel
        usepackage = '\\usepackage' + Optional('[' + Word(alphanums) + ']') + '{texsurgery}'
        self.kernel_name = usepackage.searchString(self.src, maxMatches=1)[0][2]
        usepackage.setParseAction(lambda l,s,t: '')

        run = self._parserFor('run')
        run.setParseAction(self.run)
        runsilent = self._parserFor('runsilent')
        runsilent.setParseAction(self.runsilent)
        eval = self._parserFor('\\eval', options=False)
        eval.setParseAction(self.eval)
        evalstr = self._parserFor('\\evalstr', options=False)
        evalstr.setParseAction(self.evalstr)
        sage = self._parserFor('\\sage', options=False)
        sage.setParseAction(self.sage)
        sif = self._parserFor(
            '\\sif{condition}{texif}{texelse}', options=False
        )
        sif = ('\\sif' + nestedExpr('{', '}')('condition')
                + nestedExpr('{', '}')('texif')  + nestedExpr('{', '}')('texelse')
                )
        sif.setParseAction(self.sif)
        codeparser = usepackage | run | runsilent | eval | evalstr | sage | sif
        self.src = codeparser.transformString(self.src)
        return self

    def _parserFor(self, env_or_command, options=True):
        if env_or_command[0]=='\\':
            if '[' in env_or_command:
                bracket_start =  env_or_command.find('[')
                bracket_ends  =  env_or_command.find(']')
                command_name = env_or_command[:bracket_start]
                nargs = int(env_or_command[bracket_start+1:bracket_ends])
                mandatory_args = sum(
                    (skipToMatching('{','}')('arg%d'%k) for k in range(1,1+nargs)),
                    Empty()
                )
            elif '{}' in env_or_command:
                arg = skipToMatching('{','}')
                args = (m[0][1:-1] for m in skipToMatching('{','}').searchString(selector))
                mandatory_args = sum(
                    (skipToMatching('{','}')(arg) for arg in args),
                    Empty()
                )
            else:
                command_name = env_or_command
                mandatory_args = skipToMatching('{','}')('content')
            if options:
                return (Literal(command_name)('name') +
                        Optional(skipToMatching('[',']'))('options') +
                        mandatory_args
                        )
            else:
                return (env_or_command + mandatory_args)
        else:
            return (('\\begin{' + Literal(env_or_command)('name') + '}')
                    + SkipTo('\\end{'+env_or_command+'}')('content')
                    + ('\\end{' + env_or_command + '}'))

    def findAll(self, selector, tex=None):
        tex = tex or self.src
        #First, if there is a ", " at the top level, we split there
        if ', ' in selector:
            return sum((self.findAll(subselector) for subselector in selector.split(', ')), [])
        parent, *rest = selector.split(' ', 1)
        names = Or([self._parserFor(env_or_command)
            for env_or_command in parent.split(',')])
        if rest:
            matches = [
                (match.name, self.findAll(rest[0], match.content))
                for match in names.searchString(tex)
            ]
            return [(name,nest) for (name,nest) in matches if nest]
        elif selector[0]=='\\':
            results = []
            if '[' in selector:
                bracket_start, bracket_ends  =  selector.find('['), selector.find(']')
                nargs = int(selector[bracket_start+1:bracket_ends])
                return [
                    (match.name, [match['arg%d'%k][1:-1] for k in range(1,1+nargs)])
                    for match in names.searchString(tex)
                ]
            else:
                return [
                    (match.name, match.content[1:-1])
                    for match in names.searchString(tex)
                ]
        else:
            return [
                (match.name, match.content)
                for match in names.searchString(tex)
            ]
