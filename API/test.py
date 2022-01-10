import requests
#res = requests.post('http://localhost:5000/send',json={'acc_name':'Ivan Bilenko','message':'Это сообщение отправлено через API','client_name':'Egor Izgarshev'})
#res = requests.get('http://localhost:5000/update')
#print(res.status_code)
#print(res.text)
print('https://www.linkedin.com/in/cg'.split('https://www.linkedin.com/in/')[1])

# class Pupil:
#     s = 5
#     def __init__(self):
#         self.name = 'Ivan'
#     def study(self):
#         print("Учить в зависимости от курса")
#
# class Sophmore(Pupil):
#     f = 2
#     def __init__(self):
#         super().__init__()
#         self.lena = 'Плыгунова'
#     #def study(self)
#      #   print("Учить предметы для второго курса")
#
#     return func_name
#
#
# @decorator
# def fun():
#     print('x')
#
#
# def logging(func):
#     def log_function_called():
#         print(f'{func} called.')
#         func()
#
#     return log_function_called
#
#
# @logging
# def friends_name():
#     print('naruto')
#
#
# fun()
# std = Pupil()
# std.study()
# soph = Sophmore()
# soph.study()
# print(soph.name)
# print(-12 % 10)
#
# def decorator(func):
#     def func_name():
#         print('hello gy!')
#         func()


# n = 34
# l = [1,2,'23']
# print(l)
# print(id(n),id(l))
#
# def check(n,l):
#     n = n+1
#     print(id(n))
#     l[1] = 0
#     print(id(l))
#
# check(n,l)
# print(type(int('32')))

# print(''.join(str(i) for i in range(0,100)))
#
# l = [1,1,1,2,3,4,5,6,7,7,7]
# new = []
# for i in range(len(l)):
#     if l[i] not in new:
#         new.append(l[i])
# print(new)
# print(set(l))
#
# True = False
#
# print(1 if 1 in (1,2,34) else 0)