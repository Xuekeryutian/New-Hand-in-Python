


class Operation(object):
    def __init__(self,number1 = 0,number2 = 0):
        self.num1 = number1
        self.num2 = number2


    def GetResult(self):
        pass
    pass


class OperationAdd(Operation):#加
    def GetResult(self):
        return int(self.num1) + int(self.num2)

class OperationSub(Operation):#减
    def GetResult(self):
        return int(self.num1) - int(self.num2)


class OperationMul(Operation):#乘
    def GetResult(self):
        return int(self.num1) * int(self.num2)


class OperationDiv(Operation):#除
    def GetResult(self):
        return int(self.num1) / int(self.num2)


class OperationUndef(Operation):#其他
    def GetResult(self):
        return '操作符错误'



class OperationFactory(object):
    def choose_oper(self,ch):
        if ch == '+':
            return OperationAdd()
        elif ch == '-':
            return OperationSub()
        elif ch == '*':
            return OperationMul()
        elif ch == '/':
            return OperationDiv()
        else:
            return OperationUndef()






if __name__ == "__main__":
    ch = ''
    while not ch == 'q':
        num1 = input('请输入第一个数值:   ')
        oper = str(input('请输入一个四则运算符:   '))
        num2 = input('请输入第二个数值:   ')

        OF = OperationFactory()
        oper_obj = OF.choose_oper(oper)
        oper_obj.num1 = num1
        oper_obj.num2 = num2
        print('运算结果为:   ',oper_obj.GetResult())

