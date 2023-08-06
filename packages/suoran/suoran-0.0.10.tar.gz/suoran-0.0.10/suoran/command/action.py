from . import skeleton

def start(args, options):
    '''
    '''

def stop(args, options):
    '''
    '''

def restart(args, options):
    '''
    '''
    
    stop()
    start()

def new(args, options):
    '''
    创建骨架
    '''
    
    argc = len(args)
    if argc < 1:
        print('input path of new app.')
    elif argc > 1:
        print(f'args need 1 but {argc} input')
    else:
        skeleton.unzip(args[0])
    

def init(args, options):
    '''
    初始化项目
    '''

    argc = len(args)
    if argc > 0:
        print('init not any args.')
    else:
        skeleton.unzip('.')
