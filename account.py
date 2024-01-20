from enum import Enum
from decimal import Decimal
import json

"""Объединение, описывающее базовые операции над счётом"""


class OperationType(Enum):
    Decrease = 'Decrease'
    Increase = 'Increase'


"""Объединение, описывающее наименования полей в JSON"""


class JsonFieldName(Enum):
    Actions = 'actions'
    Action = 'action'
    Value = 'value'


"""Небольшая оговорка: в задании написано следующее: 'создание банковского аккаунта с параметрами: имя, стартовый баланс с которым зарегистрирован аккаунт, история операций'. Данную фразу я интерпретирую следующем образом: в класс передается баланс при создании аккаунта и операции, которые были с ним совершены. Т.е, текущий баланс == баланс при создании аккаунта + все изменения, которые произошли с аккаунтом(т.е. история изменений). Не очень понятно, зачем в такой модели стартовый баланс(который, очевидно, при создании счета равен 0) но это, видимо, нужно для тех случаев, когда задача решается без дополнительного задания(истории операций)"""


class Account:
    def __init__(self, name: str, start_balance: Decimal = Decimal('0.00'), history_json_str: str = '{"actions":[]}'):
        self.__name = name
        self.__history = json.loads(history_json_str)
        self.__current_balance = start_balance
        self.__calculate_balance_from_history()

    def get_balance(self) -> Decimal:
        return self.__current_balance

    def get_history(self) -> str:
        return json.dumps(self.__history)

    """Увеличивает баланс счёта"""

    def increase_balance(self, value: Decimal) -> None:
        self.__current_balance += value
        self.__add_to_history(OperationType.Increase, value)

    """Уменьшает баланс счёта"""

    def decrease_balance(self, value: Decimal) -> None:
        if self.__current_balance - value < 0:
            raise ValueError('Not enough money')

        self.__current_balance -= value
        self.__add_to_history(OperationType.Decrease, value)

    def __calculate_balance_from_history(self) -> None:
        for action in self.__history[JsonFieldName.Actions.value]:
            if action[JsonFieldName.Action.value] == OperationType.Decrease.value:
                self.__current_balance -= Decimal(action[JsonFieldName.Value.value])
            if action[JsonFieldName.Action.value] == OperationType.Increase.value:
                self.__current_balance += Decimal(action[JsonFieldName.Value.value])

    def __add_to_history(self, operation_type: OperationType, value: Decimal):
        new_record = {JsonFieldName.Action.value: operation_type.value, JsonFieldName.Value.value: str(value)}
        self.__history[JsonFieldName.Actions.value].append(new_record)