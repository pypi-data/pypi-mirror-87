import os
import io
import base64
import zipfile
from ..common import list_files


def zip(folder):
    '''
    把框架压缩成字符串并写到 python 文件里。
    '''
    with io.BytesIO() as bio:
        with zipfile.ZipFile(bio, 'w') as zf:
            for p in list_files(folder):
                n = os.path.relpath(p, folder)
                if n.find('__pycache__') < 0:
                    zf.write(p, n)
        d = os.path.dirname(__file__)
        t = os.path.join(d, 'skeletonzip.py')
        r = base64.b64encode(bio.getbuffer())
        with open(t, 'w', encoding='utf8') as writer:
            writer.write(f'zip={r}')


def unzip(folder):
    '''
    解压框架。
    '''

    from . import skeletonzip
    b = base64.b64decode(skeletonzip.zip)
    with io.BytesIO(b) as bio:
        with zipfile.ZipFile(bio, 'r') as zf:
            zf.extractall(folder)
