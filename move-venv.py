#!/usr/bin/python
"""
copy a venv to a new directory.
it doesn't delete the original (that's on you)

usage:
move-venv.py <old-dir> <new-dir>

if <new> doesn't exist, copy <old> to <new>

"""

import os, re, sys, time
from os.path import expanduser, expandvars, isdir, isfile, join, basename, abspath, splitext, getsize, dirname
from os import mkdir, chdir, rename, unlink, walk
from shutil import copytree, rmtree as deltree, rmtree, which #, copyfile
from glob import glob, iglob
from liblib import usage, reg_single


# ------ CONSTs -------
flags = re.M+re.I+re.S



def run2(cmd):
    print(cmd)
    retval = os.system(cmd)
    return not retval # here non-zero is SUCCESS, zero is FAIL


def move_venv(old, new):
    """ we don't do that """
    try:
        rename(old, new)
        return True
    except:
        print("python's 'rename' failed. Trying 'mv'")
    return run2(f'mv "{old}" "{new}"')



def copy_venv(old, new):
    return run2(f'cp -rfp "{old}" "{new}"')


def guess_old_path(new):
    old = None
    if windows:
        script_dir= 'Scripts'
        f = join(new, script_dir, 'activate')
        cygwin = os.environ["OSTYPE"] in ["cygwin", "msys"]
        if cygwin:
            old = reg_single(r'export VIRTUAL_ENV=\$(cygpath "(.*?)"')
        else:
            old = reg_single(r'export VIRTUAL_ENV="(.*?)"')
    else:
        old = reg_single(r'VIRTUAL_ENV="(.*?)"')
    return old


def reset_existing_venv(old='', new='', also_basename=False):
    c=0
    if not old:
        old = guess_old_path(new)
    if old==new:
        print("error? can't tell old venv's dir. Maybe venv already reflects new directory.")
        exit(1)

    for f in glob(join(new, '*')):
        s = orig = open(f).read() # blindly assuming only plaintext files contain "old"
        s = popen(f'file "{f}"')
        if 'ELF' in s or not 'text' in d:
            print('skipping non-text: {f}')

        # sed -i "s|$old|$new|g" *
        s = s.replace(old, new)
        if also_basename:
            s = s.replace(f'({basename(old)})', f'({basename(new)})')

        if s!= orig:
            print(f'changed: "{f}"')
            open(f,'w').write(s)
            c +=1

    if c < 4:
        print(f"error: only {c} files changed! (should've been more).")
        exit(1)



def ask_for_crazy():
    items = [ 'Yes, allow (take the risk of changing irrelevant strings)',
              'No, how crazy am i?',
              'Quit']
    prompt = "Folder's base-name differs (/path/a != /path/b). Allow it? (volatile)"
    prompt += warning
    ans = interactive_menu(items, multiple=False, title='', prompt=prompt)
    if ans == 3: exit()
    return ans==1


def change_venv(old, new):
    oldbase, newbase = basename(old), basename(new)
    crazy = False

    if oldbase != newbase:
        warning = ''
        if len(oldbase) <4 or len(newbase)<4:
            warning = '\nWARNING! base names are VERY short, hence likely to match random shit in the files.'
        if re.search('[()]', oldbase+newbase, flags=flags):
            print('folder name(s) contain "()"; way above my pay grade')
        else:
            crazy = ask_for_crazy()


    if isdir(new):
        items = [   'Copy into',
                    'just fix the existing dir',
                    'Quit!']
        prompt='target "{new}" dir already exists.'
        ans = interactive_menu(items, multiple=False, title='', prompt=prompt)
        if ans==1: copy_venv(old, new)
        elif 2: pass
        else: exit()
    else: # target doesnt exist
        copy_venv(old, new)

    crazy = ask_for_crazy()
    reset_existing_venv(old, new, crazy)


if __name__=='__main__':
    args = sys.argv[1:]
    if not args:  usage('wrong arguments')
    if len(args)==1:
        crazy = ask_for_crazy()
        reset_existing_venv(new=args[0], crazy=True)
    else:
        old, new = args
        change_venv(old, new)


