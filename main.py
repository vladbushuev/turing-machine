class Tape:
    def __init__(self, tape_string="", blank_symbol=" "):
        """
        Инициализация ленты.
        :param tape_string: Начальная строка на ленте.
        :param blank_symbol: Символ, обозначающий пустую ячейку.
        """
        self.tape = list(tape_string)
        self.blank_symbol = blank_symbol
        self.head_position = 0

    def get_current_symbol(self):
        """
        Возвращает символ под головкой.
        """
        if self.head_position < 0 or self.head_position >= len(self.tape):
            return self.blank_symbol
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        """
        Пишет символ под головкой.
        """
        if self.head_position < 0:
            # Расширяем ленту влево
            self.tape = [self.blank_symbol] * (-self.head_position) + self.tape
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            # Расширяем ленту вправо
            self.tape += [self.blank_symbol] * (self.head_position - len(self.tape) + 1)
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
        """
        Перемещает головку влево (L) или вправо (R).
        """
        if direction == "L":
            self.head_position -= 1
        elif direction == "R":
            self.head_position += 1
        else:
            raise ValueError("Направление должно быть 'L' или 'R'")

    def get_tape_contents(self):
        """
        Возвращает текущие содержимое ленты.
        """
        return "".join(self.tape)


class TuringMachine:
    def __init__(self, tape, initial_state, final_states, transition_function):
        """
        Инициализация машины Тьюринга.
        :param tape: Объект типа Tape.
        :param initial_state: Начальное состояние машины.
        :param final_states: Множество конечных состояний.
        :param transition_function: Таблица переходов.
        """
        self.tape = tape
        self.current_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function
        self.step_count = 0

    def step(self):
        """
        Выполняет один шаг машины Тьюринга.
        """
        current_symbol = self.tape.get_current_symbol()
        key = (self.current_state, current_symbol)
        if key not in self.transition_function:
            return False  # Нет перехода, машина останавливается

        new_state, write_symbol, direction = self.transition_function[key]
        # Записываем символ
        self.tape.write_symbol(write_symbol)
        # Перемещаем головку
        self.tape.move_head(direction)
        # Переходим в новое состояние
        self.current_state = new_state
        self.step_count += 1
        return True

    def run(self, max_steps=1000):
        """
        Запускает выполнение машины Тьюринга до достижения конечного состояния или превышения максимального числа шагов.
        :param max_steps: Максимальное количество шагов.
        """
        while self.current_state not in self.final_states and self.step_count < max_steps:
            if not self.step():
                break
        if self.current_state in self.final_states:
            print(f"Машина остановилась в конечном состоянии '{self.current_state}' после {self.step_count} шагов.")
        else:
            print(f"Машина достигла максимального количества шагов ({max_steps}).")

    def get_configuration(self):
        """
        Возвращает текущую конфигурацию машины.
        """
        tape_str = self.tape.get_tape_contents()
        head = self.tape.head_position
        return f"Состояние: {self.current_state}\nЛента: {tape_str}\nГоловка: {head}"


# Функция для проверки палиндрома с вводом от пользователя
def palindrome_checker():
    # Ввод строки пользователем
    input_str = input("Введите строку для проверки на палиндром: ").strip().lower()

    # Добавляем специальный символ '#' для обозначения конца строки
    tape = Tape(tape_string=input_str + "#")  # '#' - символ конца строки

    # Определяем состояния
    initial_state = "q0"
    final_states = {"q_accept", "q_reject"}

    # Таблица переходов:
    # (состояние, символ) : (новое состояние, символ для записи, направление)
    transition_function = {
        # Переходы из начального состояния q0
        ("q0", "r"): ("q1", " ", "R"),
        ("q0", "a"): ("q_reject", "a", "R"),
        ("q0", "d"): ("q_reject", "d", "R"),
        ("q0", "#"): ("q_accept", "#", "R"),

        # Состояние q1: перемещение вправо до конца строки
        ("q1", "a"): ("q1", "a", "R"),
        ("q1", "d"): ("q1", "d", "R"),
        ("q1", "r"): ("q1", "r", "R"),
        ("q1", "#"): ("q2", "#", "L"),

        # Состояние q2: проверка последнего символа
        ("q2", "r"): ("q3", " ", "L"),
        ("q2", "a"): ("q_reject", "a", "L"),
        ("q2", "d"): ("q_reject", "d", "L"),

        # Состояние q3: перемещение влево для проверки в начале строки
        ("q3", "a"): ("q4", "a", "L"),
        ("q3", "d"): ("q_reject", "d", "L"),
        ("q3", " "): ("q_accept", " ", "R"),

        # Состояние q4: проверка символов
        ("q4", "a"): ("q0", "a", "R"),
        ("q4", "d"): ("q_reject", "d", "L"),
        ("q4", " "): ("q_reject", " ", "R"),
    }

    # Создаем машину Тьюринга
    machine = TuringMachine(tape, initial_state, final_states, transition_function)

    # Вывод начальной конфигурации
    print("\nНачальная конфигурация:")
    print(machine.get_configuration())

    # Запуск машины Тьюринга
    machine.run()

    # Вывод конечной конфигурации
    print("\nКонечная конфигурация:")
    print(machine.get_configuration())


if __name__ == "__main__":
    palindrome_checker()
