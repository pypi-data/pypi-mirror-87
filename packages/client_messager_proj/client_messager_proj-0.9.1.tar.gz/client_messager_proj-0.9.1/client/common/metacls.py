import dis


class ServerVerifier(type):
    """
    Метакласс контроля использования параметров
    'SOCK_STREAM' и 'AF_INET' в классах серверной части
    """
    def __init__(self, clsname, bases, clsdict):

        methods_lst = []
        attr_lst = []
        for func in clsdict:
            try:
                instruction = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in instruction:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods_lst:
                            methods_lst.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attr_lst:
                            attr_lst.append(i.argval)
        if 'connect' in methods_lst:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        if not 'SOCK_STREAM' in attr_lst and 'AF_INET' in attr_lst:
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)




class ClientVerifier(type):
    """
    Метакласс валидации использования методов
    в классах клиентской части
    """
    def __init__(self, clsname, bases, clsdict):
        methods_lst = []
        for func in clsdict:
            try:
                instruction = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in instruction:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods_lst:
                            methods_lst.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods_lst:
                raise TypeError("Методы : 'accept', 'listen', 'socket' нельзя использваоть в классе Client")

        if 'get_message' in methods_lst or 'send_message' in methods_lst:
            pass
        else:
            raise TypeError('В классе Client должны быть определенный методы :"get_message" или "send_message" ')
        super().__init__(clsname, bases, clsdict)