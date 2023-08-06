from optparse import OptionParser
from . import action

def luanch():
    '''
    命令启动
    '''

    parser = OptionParser(
        usage='suoran [action] [action-options] [arguments]',
    )
    options, args = parser.parse_args()
    if len(args) > 0:
        dispatch(args[0], args[1:], options)
    else:
        print('error: require input action.')

def dispatch(name, args, options):
    '''
    命令分发
    '''

    if hasattr(action, name):
        task = getattr(action, name)
        task(args, options)
    else:
        print('unknown action.')
    
    
    
