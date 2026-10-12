import asyncio

# async def asyn_numbers():
#     for i in range(1, 4):
#         await asyncio.sleep(1)
#         yield i
# async def main():
#     async for number in aiter(asyn_numbers()):
#         print(number)
# asyncio.run(main())

# async def websocket_mock():
#     messages = ['Hi', 'How are you?', 'Bye']
#     for msg in messages:
#         await asyncio.sleep(1)
#         yield msg
# async def main():
#     async for msg in aiter(websocket_mock()):
#         print(msg)
# asyncio.run(main())

# async def async_numbers():
#     for i in range(2):
#         yield i
# async def main():
#     agen = aiter(async_numbers())
#     while True:
#         try:
#             print(await anext(agen))
#         except StopAsyncIteration:
#             print('Generator exhausted')
#             break
# asyncio.run(main())
            
# async def process_item(item):
#     print(f"Processed {item}")
# async def main():
#     queue = ['task1', 'task2']
#     async_gen = (await process_item(item) for item in queue)
#     while True:
#         try:
#             await anext(async_gen)
#         except StopAsyncIteration:
#             print('Generator exhausted')
#             break
# asyncio.run(main())

# def debugger(a, b):
#     breakpoint()
#     result = a / b
#     return result
# print(debugger(5, 0))

# x = 10
# print(callable(x))
# def greet(x):
#     return x
# y = greet
# print(callable(y))

# class User:
#     price = 1000
#     rating = 5
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
    
#     @classmethod
#     def from_string(cls, data):
#         n, a = data.split('-')
#         return cls(n, a)
# u = User.from_string("Alex-31")
# print(u.name)
# print(u.age)

# print(User.price)
# delattr(User, 'price')
# print(User.price)
# print(User.rating)

# print(list(divmod(5,4)))

# expression = 'x*(x+1)*(x+2)'
# print(expression)
# x = 3
# result = eval(expression)
# print(result)

# print(2 ** 3)
# print(pow(2, 3))
