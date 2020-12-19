import time

# Число прогонов функции задаем константой
NUM_RUNS = 10


class Stopwatch:
    def __init__(self, num_runs=NUM_RUNS):
        self.num_runs = num_runs
        self.time_start = 0
        self.time_stop = 0
        self.avg_time = 0

    def __call__(self, func):
        def decorator():
            time_avg = 0
            for i in range(self.num_runs):
                time_begin = time.time()
                func()
                time_end = time.time()
                time_avg += time_end - time_begin
                # расскомментировать для большей детализации процесса:
                # print(i, 'проход, общее время: %.5f секунд' % time_avg)

            self.avg_time = time_avg / self.num_runs
            print("\nКоличество запусков", self.num_runs, "\nСреднее время выполнения = %.5f секунд\n" % self.avg_time)

        return decorator

    def __enter__(self):
        self.time_start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_stop = time.time()
        self.avg_time = self.time_stop - self.time_start
        # print("\nВремя выполнения = %.5f секунд\n\n" % self.avg_time)


# На вход декоратор принимает количество проходов
def time_this(num_runs):
    # Создаем собственно обертку-декоратор
    def time_run(func):
        # Фиксируем действия, которые должны выполняться
        def stopwatch():
            avg_time = 0
            print("------------------------ Декорируемая функция ------------------------")
            for i in range(num_runs):
                time_start = time.time()
                func()
                avg_time += time.time() - time_start
                # расскомментировать для большей детализации процесса:
                # print(i, 'проход, общее время: %.5f секунд' % avg_time)
            avg_time /= num_runs
            print("\nКоличество запусков", num_runs, "\nСреднее время выполнения = %.5f секунд\n" % avg_time)

        return stopwatch
    return time_run


# Декорируем исследуемую функцию
@time_this(NUM_RUNS)
def f():
    for j in range(1000000):
        pass

# Вызов функции для получения результата
f()

# Вызов функции для получения результата с декоратором в классе
print("------------------- Декорируемая в классе функция --------------------")


@Stopwatch(num_runs=NUM_RUNS)
def f_decor_class():
    for j in range(1000000):
        pass


f_decor_class()

# Получение результата контекстным менеджером
print("------------------------ Контекстный менеджер ------------------------")


@Stopwatch(num_runs=NUM_RUNS)
def f_cont_manager():
    for j in range(1000000):
        pass


with Stopwatch() as timing:
    f_cont_manager()