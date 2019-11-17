import importlib


class Controller:
    @staticmethod
    def controllerHandler(relative_path,event,context):
        print('controllerHandler')
        r= relative_path.split("/")
        cls=r[2]#要调用的类名
        meth=r[3]#要调用的方法名
        i=0;
        temp = 'contr.'+cls+''  # 要引入的模块
        print(temp)
        func = meth  # 要使用的方法
        # model = __import__(temp)  # 导入模块
        model = importlib.import_module(temp)  # 导入模块
        function = getattr(model, func)  # 找到模块中的属性
        function('helll')


# Controller.controllerHandler("/controller/aa/say",None,None)