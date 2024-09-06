# move-venv
Relocate a venv to another folder. Or try fixing it if it's already moved

# why
Python's venv isn't relative (for an unexplicable reason), and the path(s) are oddly embedded in the code.
so moving it to another directory will not work, pain to fix manually.

# caveats
 - The app relies on luck, and semi-blind string replacement in a bunch of random files;
 - we should've used a parser to find & replace dir names, but there are too many different sripts involved.
 - It's a hack.
 - it will refuse to update in some cases (will let you know)
 - it uses external system command:  `cp`.
 - Exceptions are broad / general     #   @todo #fixme
 - it might get your rabbies.

IT IS almost GUARANTEED TO FAIL.

got it?


# How
this **interactive** program will do these things:
  - copy / move old env to the new name / folder, if desired or required
  - if basename(new) vs. basename(old) is different, try a risky attempt to change even shorter strings.
  - if only 1 dir is provided, try just to fix it (reset foldernames to the full path & basename of actual given folder


