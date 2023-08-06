import importlib
import os.path

from jupyter_client.kernelspec import KernelSpecManager

from .test_simplekernel import *
from .test_data_surgery import *
from .test_imports import *

def import_kernel_tests(module_name):
    mdl = importlib.import_module(module_name, package='tests')
    # is there an __all__?  if so respect it
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        # otherwise we import all names that don't begin with _
        names = [x for x in mdl.__dict__ if not x.startswith("_")]
    globals().update({k: getattr(mdl, k) for k in names})

def test_all():
    ksm = KernelSpecManager()

    has_sagemathxx = False
    has_sagemath = False
    for k in ksm.get_all_specs():
        if k=='sagemath':
            has_sagemath = True
        elif k.startswith('sagemath') and k!='sagemath':
            has_sagemathxx = True
        try:
            print('Start tests for kernel', k)
            import_kernel_tests('.test_%s'%k)
            if os.path.exists('tests/test_%s_integration.py'%k):
                import_kernel_tests('.test_%s_integration'%k)
            print('Done')
        except:
            print('No specific tests for installed kernel ', k)
        print('-'*30)

    if has_sagemathxx and not has_sagemath:
        try:
            mod = importlib.import_module('test_sagemath.py')
        except:
            pass

test_all()
