__version__ = '000.000.053'
__author__ = 'Calafiore Carmelo'
__author_email__ = 'c.calafiore@essex.ac.uk'
__maintainer_email__ = 'c.calafiore@essex.ac.uk'
__all__ = [
    'array', 'check_args', 'clock', 'combinations', 'directory', 'download',
    'format_args', 'image', 'maths', 'mixamo', 'nn', 'plot', 'preprocessing', 'shutdown', 'stats',
    'stimulation', 'strings', 'txt']


def initiate(names_submodules=None):
    template_import_string = "from . import "
    if isinstance(names_submodules, str):
        import_string_m = template_import_string + names_submodules
        exec(import_string_m)
    elif isinstance(names_submodules, (list, tuple)):
        for name_m in names_submodules:
            if isinstance(name_m, str):
                import_string_m = template_import_string + name_m
            else:
                import_string_m = template_import_string + str(name_m)
            exec(import_string_m)
    elif names_submodules is None:
        exec('from . import *')
        # for name_m in __all__:
        #     if isinstance(name_m, str):
        #         import_string_m = template_import_string + name_m
        #     else:
        #         import_string_m = template_import_string + str(name_m)
        #     exec(import_string_m)
    else:
        raise TypeError(names_submodules)
