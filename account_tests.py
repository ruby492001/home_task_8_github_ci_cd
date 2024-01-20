from account import Account
import unittest
from decimal import Decimal


# Тест корректности рассчётов
def test_correct_calculate_balance() -> None:
    account_1 = Account('Fedor')
    account_1.increase_balance(Decimal('60000.00'))
    account_1.decrease_balance(Decimal('30000.00'))
    account_1.increase_balance(Decimal('5000.00'))
    account_1.decrease_balance(Decimal('12345.22'))

    assert account_1.get_balance() == Decimal('22654.78')


# Тест корректности восстановления баланса из сохраненной строчки и корректная работа объекта после этого
def test_restore_from_string() -> None:
    account_1 = Account('Fedor')
    account_1.increase_balance(Decimal('60000.00'))
    account_1.decrease_balance(Decimal('30000.00'))
    account_1.increase_balance(Decimal('5000.00'))
    account_1.decrease_balance(Decimal('12345.22'))

    account_1_restored = Account('Fedor', history_json_str=account_1.get_history())
    account_1_restored.increase_balance(Decimal('12345.22'))
    account_1_restored.decrease_balance(Decimal('10200.00'))

    assert account_1_restored.get_balance() == Decimal('24800.00')


# Класс для тестирования уменьшения баланса
class DecreaseTestCase(unittest.TestCase):
    def __init__(self):
        super(DecreaseTestCase, self).__init__()

    def test_decrease_balance(self, init_balance: Decimal, decrease_summ: Decimal, error_must_occur: bool) -> None:
        account_1 = Account('Fedor', init_balance)
        if error_must_occur:
            self.assertRaises(ValueError, account_1.decrease_balance, decrease_summ)
        else:
            except_occur = False
            try:
                account_1.decrease_balance(decrease_summ)
            except ValueError:
                except_occur = True

            assert except_occur == False


if __name__ == '__main__':
    test_correct_calculate_balance()
    test_restore_from_string()

    t = DecreaseTestCase()
    t.test_decrease_balance(Decimal('5000'), Decimal('4000'), False)
    t.test_decrease_balance(Decimal('5000'), Decimal('6000'), True)
    t.test_decrease_balance(Decimal('5000'), Decimal('4999'), True)
    t.test_decrease_balance(Decimal('5000'), Decimal('4999'), False)
    t.test_decrease_balance(Decimal('5000'), Decimal('5001'), True)
