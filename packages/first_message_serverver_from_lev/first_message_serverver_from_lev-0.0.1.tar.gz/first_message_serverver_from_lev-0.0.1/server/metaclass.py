import dis

class ServerMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        methods2 = []
        attrs = []

        for func in clsdict:
            try:
                ret = dis.get_instructions(func)
            except TypeError:
                pass
            else:
                for i in ret:
                    # print(i)
                    if i.opname == 'LOAD_NAME':
                        # print(i)
                        if i.argval not in methods:
                            # print(i.argval)
                            methods.append(i.argval)
        # print(methods)
        for i in methods:
            try:
                res1 = dis.get_instructions(clsdict[i])
            except:
                pass
            else:
                for g in res1:
                    # print(g)
                    if g.opname == 'LOAD_METHOD':
                        if g.argval not in methods2:
                            methods2.append(g.argval)
                    if g.opname == 'LOAD_GLOBAL':
                        if g.argval not in attrs:
                            attrs.append(g.argval)
                    # print(g)
        # print(methods2)
        # print(f'Attrs {attrs}')
        if 'connect' not in methods2:
            print('None method connect')
        if 'AF_INET' not in attrs:
            print('Error AF_NET')
        # print('--')
        super().__init__(clsname, bases, clsdict)



class ClientMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        methods2 = []
        attrs = []

        for func in clsdict:
            try:
                ret = dis.get_instructions(func)
            except TypeError:
                pass
            else:
                for i in ret:
                    # print(i)
                    if i.opname == 'LOAD_NAME':
                        # print(i)
                        if i.argval not in methods:
                            # print(i.argval)
                            methods.append(i.argval)
        # print(methods)
        for i in methods:
            try:
                res1 = dis.get_instructions(clsdict[i])
            except:
                pass
            else:
                for g in res1:
                    # print(g)
                    if g.opname == 'LOAD_METHOD':
                        if g.argval not in methods2:
                            methods2.append(g.argval)
                    if g.opname == 'LOAD_GLOBAL':
                        if g.argval not in attrs:
                            attrs.append(g.argval)
                    # print(g)
        # print(methods2)
        # print(f'Attrs {attrs}')
        if 'accept' in methods2:
            print('Arror accept ')
        if 'listen' in methods2:
            print('Error listen')
        super().__init__(clsname, bases, clsdict)


def Dis_test(func):
    func = func
    methods = []
    attr = []
    res1 = dis.get_instructions(func)
    for i in res1:
        if i.opname == 'LOAD_GLOBAL':
            if i.opname not in methods:
                methods.append(i.argval)
        if i.opname == 'LOAD_ATTR':
            if i.opname not in attr:
                attr.append(i.argval)
    # print('---')
    # print(f'Methods - {methods}')
    # print(f'Attr - {attr}')
    # print('---')

    if 'accept' in methods:
        print('Arror accept ')
    if 'listen' in methods:
        print('Error listen')
    if 'AF_INET' not in attr:
        print('Client Exeption AF_INET')



