from functools import partial


class Super:
    def __init__(self, sub_cls, instance):
        # 假设 sub_cls = B, instance = D()
        # Super(B, self).add(233)
        mro = instance.__class__.mro()
        # mro == [D, B, C, A, object]
        # sub_cls is B
        # 从 mro 中 sub_cls 后面的类中进行查找
        # __mro_tail == [C, A, object]
        self.__mro_tail = mro[mro.index(sub_cls) + 1:]
        self.__sub_cls = sub_cls
        self.__instance = instance

    def __getattr__(self, name):
        # 从 mro tail 列表的各个类中查找方法
        for cls in self.__mro_tail:
            if not hasattr(cls, name):
                continue

            print('call {}.{}'.format(cls, name))
            # 获取类中定义的方法
            attr = getattr(cls, name)
            # 因为 d = D(); d.add(233)  等价于 D.add(d, 233)
            # 所以返回的函数需要自动填充第一个 self 参数
            return partial(attr, self.__instance)

        raise AttributeError(name)


class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        Super(B, self).add(m)
        self.n += 3


class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        Super(C, self).add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        Super(D, self).add(m)
        self.n += 5


class E(C, A):  # can`t be E(A,C)

    def __init__(self):
        self.n = 6

    def add(self, m):
        print('self is {0} @E.add'.format(self))
        Super(E, self).add(m)
        self.n += 6


if __name__ == "__main__":
    # b = B()
    # b.add(2)
    # print(b.n)
    # d = D()
    # d.add(2)
    # print(d.n)
    e = E()
    e.add(2)
    print(e.n)
