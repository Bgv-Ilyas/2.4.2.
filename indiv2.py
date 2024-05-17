from fractions import Fraction as Frac

class Pair:
    MAX_SIZE = 10  # Максимально возможный размер списка
    
    def __init__(self, first, second, max_size=MAX_SIZE):
        if not isinstance(first, int) or first <= 0:
            raise ValueError("Поле first должно быть положительным целым числом.")
        if isinstance(second, str):
            second = Frac(second)
        elif not isinstance(second, (float, int, Frac)) or second <= 0:
            raise ValueError("Поле second должно быть положительным дробным числом или строкой-дробью.")
        
        self.first = first
        self.second = float(second)
        self.max_size = min(max_size, Pair.MAX_SIZE)
        self.list = [0] * self.max_size
        self.count = 0

    def read(self):
        try:
            self.first = int(input("Введите положительное целое число для first: "))
            if self.first <= 0:
                raise ValueError
        except ValueError:
            print("Некорректный ввод для поля first. Ожидается положительное целое число.")
            return
        try:
            second_input = input("Введите положительное дробное число или дробь в формате 'a/b' для second: ")
            self.second = float(Frac(second_input) if '/' in second_input else second_input)
            if self.second <= 0:
                raise ValueError
        except (ValueError, ZeroDivisionError):
            print("Некорректный ввод для поля second. Ожидается положительное дробное число или дробь.")
            return

    def display(self):
        print(f"first: {self.first}, second: {self.second}, list: {self.list}, count: {self.count}")

    def power(self):
        return self.first * self.second * 10

    def get_max_size(self):
        return self.max_size

    def __getitem__(self, index):
        if not 0 <= index < self.max_size:
            raise IndexError("Индекс выходит за пределы списка.")
        return self.list[index]

    def __setitem__(self, index, value):
        if not 0 <= index < self.max_size:
            raise IndexError("Индекс выходит за пределы списка.")
        self.list[index] = value
        self.count = sum(1 for x in self.list if x != 0)

    def __repr__(self):
        return f"Pair(first={self.first}, second={self.second}, list={self.list}, max_size={self.max_size}, count={self.count})"

def make_pair(first, second):
    try:
        return Pair(first, second)
    except ValueError as e:
        print(e)
        return None

if __name__ == '__main__':
    pair1 = make_pair(150, "1/2")
    pair2 = make_pair(100, "1/3")

    if pair1 and pair2:
        pair1.display()
        print(f"Общая калорийность продукта: {pair1.power()} ккал")
        
        pair2.display()
        print(f"Общая калорийность продукта: {pair2.power()} ккал")
        
        pair1[0] = 5
        pair1[1] = 3
        pair1.display()
        print(f"Значение по индексу 0: {pair1[0]}")
        print(f"Значение по индексу 1: {pair1[1]}")
        print(f"Максимальный размер списка: {pair1.get_max_size()}, количество элементов: {pair1.count}")

    new_pair = Pair(100, "1/3")
    new_pair.read()
    new_pair.display()
    print(f"Общая калорийность продукта: {new_pair.power()} ккал")
class Fraction:
    def __init__(self, integer_part, fractional_part):
        self.integer_part = list(map(int, reversed(str(integer_part))))
        self.fractional_part = list(map(int, str(fractional_part)))
        self.size_int = len(self.integer_part)
        self.size_frac = len(self.fractional_part)

    def __repr__(self):
        int_part = ''.join(map(str, reversed(self.integer_part)))
        frac_part = ''.join(map(str, self.fractional_part))
        return f"{int_part}.{frac_part}"

    def __add__(self, other):
        return self._combine(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self._combine(other, lambda a, b: a - b)

    def __mul__(self, other):
        int1 = int(''.join(map(str, reversed(self.integer_part))))
        frac1 = int(''.join(map(str, self.fractional_part)))
        int2 = int(''.join(map(str, reversed(other.integer_part))))
        frac2 = int(''.join(map(str, other.fractional_part)))
        product = (int1 * (10 ** self.size_frac) + frac1) * (int2 * (10 ** other.size_frac) + frac2)
        int_product = product // (10 ** (self.size_frac + other.size_frac))
        frac_product = product % (10 ** (self.size_frac + other.size_frac))
        return Fraction(str(int_product), str(frac_product))

    def _combine(self, other, operation):
        if not isinstance(other, Fraction):
            raise TypeError("Операция поддерживается только между объектами Fraction.")
        int_res = self._operate_lists(self.integer_part, other.integer_part, operation)
        frac_res = self._operate_lists(self.fractional_part, other.fractional_part, operation)
        if len(frac_res) > self.size_frac:
            carry = frac_res.pop()
            int_res = self._operate_lists(int_res, [carry], lambda a, b: a + b)
        return Fraction(''.join(map(str, reversed(int_res))), ''.join(map(str, frac_res)))

    def _operate_lists(self, list1, list2, operation):
        max_len = max(len(list1), len(list2))
        result, carry = [], 0
        for i in range(max_len):
            digit1, digit2 = (list1[i] if i < len(list1) else 0), (list2[i] if i < len(list2) else 0)
            total = operation(digit1, digit2) + carry
            carry, total = divmod(total + 10, 10) if total < 0 else divmod(total, 10)
            result.append(total)
        if carry > 0:
            result.append(carry)
        return result

if __name__ == '__main__':
    frac1 = Fraction(123, 456)
    frac2 = Fraction(789, 123)
    print(f"Дробь 1: {frac1}")
    print(f"Дробь 2: {frac2}")
    
    frac_sum = frac1 + frac2
    print(f"Сумма дробей: {frac_sum}")
    
    frac_diff = frac1 - frac2
    print(f"Разность дробей: {frac_diff}")
    
    frac_prod = frac1 * frac2
    print(f"Произведение дробей: {frac_prod}")
