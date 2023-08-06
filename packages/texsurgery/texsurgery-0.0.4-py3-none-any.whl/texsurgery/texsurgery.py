# -*- coding: utf-8 -*-
from .simplekernel import SimpleKernel
from pyparsing import nestedExpr, Optional, Word, alphanums, originalTextFor, Literal, SkipTo

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
        #lazy
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

    def add_import(self, package, options):
        #TODO
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
        #TODO 'image/png'
        #TODO do something special with 'text/html'?
        return '\n'.join(
            r.get('text/plain') or r.get('text/html') or r.get('error')
            for r in results
        )

    def runsilent(self, l, s, t):
        self.kernel.executesilent(t.code)
        return ''

    def run(self, l, s, t):
        return self.latexify(self.kernel.execute(t.code, allow_errors=True))

    def eval(self, l, s, t):
        code =  t[1][1:-1]
        return self.latexify(self.kernel.execute(code))

    def sage(self, l, s, t):
        code =  t[1][1:-1]
        return self.latexify(self.kernel.execute('latex(%s)'%code))

    def sif(self, l, s, t):
        return t.texif

    def code_surgery(self):
        # Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        #  or whatever interactive command line application
        # Use pyparsing as in student_surgery to go through sage|sagestr|sagesilent|sif|schoose in order
        # Use SimpleKernel to comunicate with a sage process ?

        # TODO Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        usepackage = '\\usepackage' + Optional('[' + Word(alphanums) + ']') + '{texsurgery}'
        self.kernel_name = usepackage.searchString(self.src, maxMatches=1)[0][2]
        usepackage.setParseAction(lambda l,s,t: '')

        #TODO?? first pass for synonims sage->eval sagesilent->runsilent
        #slow
        run = '\\begin{run}' + SkipTo('\\end{run}')('code') + '\\end{run}'
        run.setParseAction(self.run)
        runsilent = ('\\begin{runsilent}'
                     + SkipTo('\\end{runsilent}')('code')
                     + '\\end{runsilent}')
        runsilent.setParseAction(self.runsilent)
        eval = '\\eval' + skipToMatching('{', '}')
        eval.setParseAction(self.eval)
        sage = '\\sage' + skipToMatching('{', '}')
        sage.setParseAction(self.eval)
        sif = ('\\sif' + nestedExpr('{', '}')('condition')
                + nestedExpr('{', '}')('texif')  + nestedExpr('{', '}')('texelse')
                )
        sif.setParseAction(self.sif)
        codeparser = usepackage | run | runsilent | eval | sage | sif
        self.src = codeparser.transformString(self.src)
        return self
