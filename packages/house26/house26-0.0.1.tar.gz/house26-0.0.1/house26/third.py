class Animal:
    '''静态变量'''
    count = 0
    
    def __init__(self, name, color):
        '''构造方法'''
        self.__name = name #私有的实例变量
        self.color = color #公有的实例变量
        print('create an animal')
        
    def get_name(self):
        '''get方法'''
        return self.__name
    
    def set_name(self, name):
        '''set方法'''
        self.__name = name