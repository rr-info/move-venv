import inspect, sys, re

MSI = re.M+re.S+re.I

def usage(msg='', doc='', error_code=0, resume=False):
    #'doc' is usually the __doc__ (docstring)
    if not doc:
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        doc = mod.__doc__
    print(doc)
    print(msg)
    if not resume:
        sys.exit(error_code)


def reg_single(reg, in_text, flags=MSI, default=''):
    if isinstance(reg, re.Pattern):
        a = reg.findall(in_text)
    else:
        a = re.findall(reg, in_text, flags=flags)
    if a:
        return a[0]
    else:
        return default



def interactive_menu(items, title='', prompt=''):
    """ options: list, tuple, set """
    title = 'choose an index or an item: '
    if not prompt:
        prompt = 'choose one option: '

    menu = title + '\n---------------------\n'
    ans = ''
    options = {}

    for i, item in enumerate(items):
        i+=1  # from 0-based to 1 based.
        menu += f'({i}) {item}\n'
        options[str(i)] = item
        options[item] = item

    while True:
        print(menu)
        ans = input(prompt).strip()
        if not ans: continue
        if ans in ['q', 'quit', 'exit', ]: exit()
        if ans in options:
            return ans
        print('no valid options')
        continue


def popen(cmd):
    return os.popen(cmd).read()

