# # class Context():
# #     def __init__(self, x,y) -> None:
# #         self.x = x
# #         self.y = y
# #         self.k = 9

# #     def embed(self, k):
# #         k.x = 4

# #     def get_k(self):
# #         return self.k
    
# #     def set_z(self):
# #         self.z= 9

# # c = Context(4,5)
# # c.set_z()
# # print(c.z)

# # dict = {c:5}
# # dict[c]

# # class AttrDict(dict):
# #     def __init__(self, *args, **kwargs):
# #         super(AttrDict, self).__init__(*args, **kwargs)
# #         self.__dict__ = self
    
# #     def __missing__(self, key):
# #         # self[key]={}
# #         return 9
    
# #     def __repr__(self):
# #         return "{0}".format(self.__dict__)
        

# # b = AttrDict()

# # b['a'] = b['a']
# # # c = c['c']

# # print(b.keys())
# # print(b)
# # # c = Context(4,5)


# # def init(context):
# #     context.k = 0


# # c.init = init
# # c.embed(c)
# # print(c.x)


# # def f(a=None, **arg):
# #     b = a
# #     print(arg)
# #     return b


# # b = f(**{'a':5})
# # print(b)

# # def init(c):
# #     c.e=0
# #     pass


# # k = c.get_k
# # print(k())
# # c.k=5
# # print(k())
# # 
# # class A():
# #     pass


# # def loopy():
# #     a = A()
# #     a.m=0
# #     def inner_loop():
# #         for i in range(2):
# #             print('output i')
# #             yield i

# #         for k in range(2):
# #             a.m +=1
# #             print('after innerloop')

# #     for i in inner_loop():
# #         yield i
    
# #     print('m')    
# #     yield a.m


# # for i in loopy():
# #     print(i)

# def kwargs(a, **other):
#     for k, v in other.items():
#         print(v)
    
#     return a

# kwargs(4, **{'o':1})

def test(a=0):
    return a


print(test(**{'a' : 1}))