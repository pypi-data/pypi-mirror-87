import os
from suoran.common import list_files
from suoran.command.skeleton import zip, unzip

for p in list_files('skeleton'):
    print(os.path.relpath(p, 'skeleton'))

# zip('skeleton')
# unzip()
