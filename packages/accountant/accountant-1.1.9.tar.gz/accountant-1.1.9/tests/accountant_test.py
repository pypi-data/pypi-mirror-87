import unittest
from accountant.client import Accountant,ErrorCodes
import random


class TestCasesOrdersAccountant(unittest.TestCase):
    def setUp(self) -> None:
        bank_account = {
            'account_id': 'test_account_id_1',
            'ledger_books': {
                'blocked_balance': {
                    'id': '2'
                },
                'main_balance': {
                    'id': '3'
                }
            }
        }
        self.accountant = Accountant(ledger_host='http://0.0.0.0:3000', bank_account=bank_account)

    def test_block_for_order(self):
        order_id = "605"
        order_type = 'limit'
        currency = 'inr'
        value = '100'
        operation = self.accountant.block_for_order(order_id, order_type, currency, value)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')

    def test_update_order_fill_status(self):
        order_id = "605"
        from_currency = 'inr'
        to_currency = 'btc'
        from_amount = '40'
        to_amount = '40'
        memo = '102'
        order_type = 'limit'
        operation = self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount, to_amount, memo)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')

    def test_get_order_fill_status_in_bulk(self):
        order_list = ["605"]
        fill_statuses = self.accountant.get_order_fill_status_in_bulk(order_list)
        print(fill_statuses)

    def test_unblock_for_order(self):
        order_id = "605"
        order_type = 'limit'
        operation = self.accountant.unblock_for_order(order_id, order_type)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')

    def test_flow_1(self):
        """Trying to unblock funds for an orderId for which funds were never blocked"""
        order_id = str(random.randint(1, 10000))
        order_type = 'limit'
        self.assertRaisesRegexp(Exception, ErrorCodes.INSUFFICIENT_FUNDS.value, self.accountant.unblock_for_order, order_id, order_type)

    def test_flow_2(self):
        """Trying to fill funds for an orderId for which funds were never blocked"""
        order_id = str(random.randint(1, 10000))
        from_currency = 'inr'
        to_currency = 'btc'
        from_amount = '10'
        to_amount = '1'
        memo = 'limit_101'
        order_type = 'limit'
        self.assertRaisesRegexp(Exception, ErrorCodes.INSUFFICIENT_FUNDS.value, self.accountant.update_order_fill_status,order_id,
                                order_type, from_currency, to_currency, from_amount, to_amount, memo )

    def test_flow_3(self):
        """Trying to unblock funds immediately after blocking funds"""
        order_id = str(random.randint(1, 10000))
        order_type = 'limit'
        from_currency = 'inr'
        from_amount = '100'
        self.accountant.block_for_order(order_id, order_type, from_currency, from_amount)
        operation = self.accountant.unblock_for_order(order_id, order_type)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')

    def test_flow_4(self):
        """Trying to unblock funds after blocking funds but before filling funds"""
        order_id = str(random.randint(1, 10000))
        order_type = 'limit'
        from_currency = 'inr'
        from_amount = '100'
        self.accountant.block_for_order(order_id, order_type, from_currency, from_amount)
        self.accountant.unblock_for_order(order_id, order_type)
        to_currency = 'btc'
        from_amount = '10'
        to_amount = '1'
        memo = 'limit_101'
        self.assertRaisesRegexp(Exception, ErrorCodes.INSUFFICIENT_FUNDS.value,
                                self.accountant.update_order_fill_status,
                                order_id, order_type, from_currency, to_currency, from_amount, to_amount, memo)

    def test_flow_5(self):
        """Trying to fill funds after blocking funds iteratively"""
        order_id = str(random.randint(1,10000))
        order_type = 'limit'
        from_currency = 'inr'
        from_amount = '100'
        self.accountant.block_for_order(order_id, order_type, from_currency, from_amount)
        to_currency = 'btc'
        from_amount = '10'
        to_amount = '1'
        memo = 'limit_101'
        self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount,
                                                 to_amount, memo)
        from_amount = '20'
        to_amount = '2'
        memo = 'limit_102'
        self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount,
                                                 to_amount, memo)
        from_amount = '30'
        to_amount = '3'
        memo = 'limit_102'
        operation = self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount,
                                                 to_amount, memo)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')

    def test_flow_6(self):
        """Trying to fill funds after blocking funds iteratively but in wrong sequence"""
        order_id = str(random.randint(1, 10000))
        order_type = 'limit'
        from_currency = 'inr'
        from_amount = '100'
        self.accountant.block_for_order(order_id, order_type, from_currency, from_amount)
        to_currency = 'btc'
        from_amount = '20'
        to_amount = '2'
        memo = 'limit_102'
        self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount,
                                                 to_amount, memo)
        from_amount = '10'
        to_amount = '1'
        memo = 'limit_102'
        self.assertRaisesRegexp(Exception, ErrorCodes.FILL_REQUEST_SEQUENCE_ERROR.value, self.accountant.update_order_fill_status,
                                order_id, order_type, from_currency, to_currency, from_amount, to_amount, memo)

    def test_flow_7(self):
        """Fill to_currency completely but leave some from_currency left in block book and revert it back to main book"""
        order_id = str(random.randint(1,10000))
        order_type = 'limit'
        from_currency = 'inr'
        from_amount = '100'
        self.accountant.block_for_order(order_id, order_type, from_currency, from_amount)
        to_currency = 'btc'
        from_amount = '90'
        to_amount = '10'
        memo = 'limit_102'
        self.accountant.update_order_fill_status(order_id, order_type, from_currency, to_currency, from_amount,
                                                 to_amount, memo)
        operation = self.accountant.unblock_for_order(order_id,order_type)
        self.assertIn("status", operation)
        self.assertEqual(operation['status'], 'APPLIED')


if __name__ == '__main__':
    unittest.main()
