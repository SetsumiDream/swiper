def fibs():
    yield 1  # 1
    print('运行次数')
    fibs_ = fibs()

    yield next(fibs_)  # 1
    fibs__ = fibs()
    print('运行次数')
    print(map(lambda a, b: a + b ,fibs_, fibs__))
    for fib in map(lambda a, b: a + b ,fibs_, fibs__):
        yield fib

f1 = fibs()
print(next(f1))
print(next(f1))
print(next(f1))
print(next(f1))
print(next(f1))
print(next(f1))
print(next(f1))