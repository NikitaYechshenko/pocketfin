def my_decorator(func):
    def wrapper():
        print("--- Логика ДО выполнения функции ---")
        func()
        print("--- Логика ПОСЛЕ выполнения функции ---")
    return wrapper

@my_decorator
def say_hello():
    print("Привет!")

say_hello()