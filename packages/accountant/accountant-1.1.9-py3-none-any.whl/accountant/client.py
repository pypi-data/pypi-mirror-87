from ledger.client import LedgerClient, OperationType
from decimal import Decimal
from enum import Enum

import logging

log = logging.getLogger(__name__)


class ErrorCodes(Enum):
    FETCH_ORDER_STATUS_ERROR = 'Error while fetching fill statuses'
    INSUFFICIENT_FUNDS = 'Insufficient funds'
    FILL_REQUEST_SEQUENCE_ERROR = 'Fill request sequence error'


class Accountant:
    """
    Accountant binds together 2 concepts - BankAccount & Ledger
    Ledger is the source of truth for the Bank
    Ledger ALWAYS reflect the true state of the OutsideWorld
    Accountant MUST manage BankAccount's books inside Ledger properly
    Accountant stores no state
    """
    DEFAULT_CASH_BOOK_ID = {'name': 'cash_book', 'id': '1'}

    def __init__(self, bank_account, ledger_host, ledger_read_host=None):
        self.bank_account = bank_account
        self.ledger = LedgerClient(ledger_endpoint=ledger_host, ledger_read_only_endpoint=ledger_read_host)

        log.info("---------Initialising-------------")
        log.info(f"Bank Account Number:  {self.bank_account['account_id']}")
        log.info(f"Cash Book:  {self.DEFAULT_CASH_BOOK_ID}")

    def get_book(self, timestamp: int = None):
        log.info("---------Get Book----------")
        blocked_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], timestamp=timestamp)['balances']
        main_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['main_balance']['id'], timestamp=timestamp)['balances']
        blocked_balance_deposit_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'DEPOSIT'}, timestamp=timestamp)
        blocked_balance_withdraw_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'WITHDRAW'}, timestamp=timestamp)
        blocked_balance_order_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'ORDER'}, timestamp=timestamp)
        book_balance = []
        for currency, amount in blocked_balance_book.items():
            if currency in main_balance_book:
                main_balance = main_balance_book[currency]
            else:
                main_balance = "0"
            if currency in blocked_balance_deposit_book:
                blocked_balance_deposit = blocked_balance_deposit_book[currency]
            else:
                blocked_balance_deposit = "0"
            if currency in blocked_balance_withdraw_book:
                blocked_balance_withdraw = blocked_balance_withdraw_book[currency]
            else:
                blocked_balance_withdraw = "0"
            if currency in blocked_balance_order_book:
                blocked_balance_order = blocked_balance_order_book[currency]
            else:
                blocked_balance_order = "0"
            balance = {
                'currency': currency,
                'blocked_balance_deposit': blocked_balance_deposit,
                'blocked_balance_withdraw': blocked_balance_withdraw,
                'blocked_balance_order': blocked_balance_order,
                'main_balance': main_balance
            }
            book_balance.append(dict(balance))
        return book_balance

    def get_book_balances(self, currency: str, metadata_filter: dict = {}, timestamp: int = None):
        log.info("---------Balance----------")
        blocked_deposit_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={**{'operation': 'DEPOSIT'}, **metadata_filter}, timestamp=timestamp)
        blocked_withdraw_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={**{'operation': 'WITHDRAW'}, **metadata_filter}, timestamp=timestamp)
        blocked_order_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={**{'operation': 'ORDER'}, **metadata_filter}, timestamp=timestamp)
        main_balance = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['main_balance']['id'],
                                                     asset_id=currency, metadata_filter={**metadata_filter}, timestamp=timestamp)
        return {'currency': currency,
                'blocked_balance_deposit': blocked_deposit_balance.get(currency, "0"),
                'blocked_balance_withdraw': blocked_withdraw_balance.get(currency, "0"),
                'blocked_balance_order': blocked_order_balance.get(currency, "0"),
                'main_balance': main_balance.get(currency, "0")}

    def withdraw_block_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Block_Amount_Withdraw----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['main_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={**{"operation": "WITHDRAW"}, **metadata})
        log.info(operation)
        return operation

    def deposit_block_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Block_Amount_Deposit----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={**{'operation': 'DEPOSIT'}, **metadata})
        log.info(operation)
        return operation

    def withdraw_unblock_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Unblock_Amount_Withdraw----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['main_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={**{'operation': 'WITHDRAW'}, **metadata})
        log.info(operation)
        return operation

    def deposit_unblock_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Unblock_Amount_Deposit----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'], asset_id=currency, value=value, memo=memo,
            metadata={**{'operation': 'DEPOSIT'}, **metadata})
        log.info(operation)
        return operation

    def withdraw_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Withdraw_amount----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            asset_id=currency, value=value, memo=memo, metadata={**{'operation': 'WITHDRAW'}, **metadata})
        log.info(operation)
        return operation

    def deposit_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Deposit_amount----------")
        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books'][
                'main_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={**{'operation': 'DEPOSIT'}, **metadata})
        log.info(operation)
        return operation

    def block_trade_amount(self, from_currency: str, to_currency: str, from_amount: str, to_amount: str, memo: str, metadata: dict = {}):
        log.info("---------Block_Trade_Amount----------")
        withdraw_block_amount = self.withdraw_block_amount(value=from_amount, currency=from_currency, memo=memo + "_WITHDRAW_BLOCK", metadata=metadata)
        deposit_block_amount = self.deposit_block_amount(value=to_amount, currency=to_currency, memo=memo + "_DEPOSIT_BLOCK", metadata=metadata)
        operation = {
            'withdraw_block_amount': withdraw_block_amount,
            'deposit_block_amount': deposit_block_amount
        }
        log.info(operation)
        return operation

    def trade_amount(self, from_currency: str, to_currency: str, from_amount: str, to_amount: str, memo: str, metadata: dict = {}):
        log.info("---------Trade_Amount----------")
        withdraw_amount = self.withdraw_amount(value=from_amount, currency=from_currency, memo=memo + "_WITHDRAW", metadata=metadata)
        deposit_amount = self.deposit_amount(value=to_amount, currency=to_currency, memo=memo + "_DEPOSIT", metadata=metadata)
        operation = {
            'withdraw_block_amount': withdraw_amount,
            'deposit_block_amount': deposit_amount
        }
        log.info(operation)
        return operation

    def freeze_books(self):
        log.info("---------Freezing Ledger Books----------")
        blocked_book = self.ledger.freeze_book(self.bank_account['ledger_books']['blocked_balance']['id'])
        main_book = self.ledger.freeze_book(self.bank_account['ledger_books']['main_balance']['id'])
        log.info(blocked_book, main_book)
        return main_book, blocked_book

    def unfreeze_books(self):
        log.info("---------Unfreezing Ledger Books----------")
        blocked_book = self.ledger.unfreeze_book(self.bank_account['ledger_books']['blocked_balance']['id'])
        main_book = self.ledger.unfreeze_book(self.bank_account['ledger_books']['main_balance']['id'])
        log.info(blocked_book, main_book)
        return main_book, blocked_book

    @staticmethod
    def create_book(account_id: str, ledger_host):
        log.info("---------New_ledger-------------")
        ledger = LedgerClient(ledger_endpoint=ledger_host)
        block_book_id = ledger.create_book(name=f"{account_id}_block_book", min_balance="0")
        main_book_id = ledger.create_book(name=f"{account_id}_main_book", min_balance="0")
        new_books = {
            'main_balance': {'name': main_book_id['name'],
                             'id': main_book_id['id']},
            'blocked_balance': {'name': block_book_id['name'],
                                'id': block_book_id['id']}
        }
        log.info(new_books)
        return new_books

    def block_for_order(self, order_id: str, order_type: str, currency: str, value: str, metadata: dict = {}):
        log.info("---------Block_Limit_Order_Funds----------")

        memo = f"{order_id}_BLOCK_ORDER"

        metadata['order_id'] = order_id
        metadata['order_type'] = order_type
        metadata['operation'] = 'ORDER'
        metadata['from_currency'] = currency
        metadata['type'] = 'BLOCK'

        operation = self.ledger.post_transfer(
            from_book_id=self.bank_account['ledger_books']['main_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency,
            value=value,
            memo=memo,
            metadata=metadata
        )

        log.info(operation)
        return operation

    def get_book_balances_bulk(self, fetch_details: list):
        query = []
        for fetch in fetch_details:
            query.append(
                {
                    'book_id': fetch['book_id'],
                    'metadata_filter': fetch['metadata_filter']
                }
            )
        balance_list = self.ledger.get_book_balances_bulk(query)
        return balance_list

    def unblock_for_order(self, order_id: str, order_type: str, metadata: dict = {}):
        log.info("---------Unblock_Limit_Order_Funds----------")

        memo = f"{order_id}_UNBLOCK_ORDER"

        block_book_order_balances = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            metadata_filter={
                "order_id": order_id
            }
        )

        if block_book_order_balances == {}:
            raise Exception(ErrorCodes.INSUFFICIENT_FUNDS.value)

        metadata['order_id'] = order_id
        metadata['order_type'] = order_type
        metadata['type'] = 'UNBLOCK'
        metadata['operation'] = 'ORDER'

        entries = []
        for asset, value in block_book_order_balances.items():
            entries.extend([
                {
                    "bookId": self.bank_account['ledger_books']['blocked_balance']['id'],
                    "assetId": asset,
                    "value": str(Decimal(value) * Decimal("-1"))
                },
                {
                    "bookId": self.bank_account['ledger_books']['main_balance']['id'],
                    "assetId": asset,
                    "value": str(Decimal(value))
                }
            ])

        operation = self.ledger.post_operation(OperationType.CUSTOM, entries, memo, metadata)
        log.info(operation)
        return operation

    def update_order_fill_status(self, order_id, order_type: str, from_currency: str, to_currency: str, from_amount: str, to_amount: str, memo: str, metadata: dict = {}):
        log.info("---------Update_Limit_Order_Funds----------")

        memo = f"{memo}_{order_id}_FILL_ORDER"

        [main_book_order_balances, block_book_order_balances, cash_book_order_balances] = self.get_book_balances_bulk([
            {
                'book_id': self.bank_account['ledger_books']['main_balance']['id'],
                'metadata_filter': {'order_id': order_id}
            },
            {
                'book_id': self.bank_account['ledger_books']['blocked_balance']['id'],
                'metadata_filter':{'order_id':order_id}
            },
            {
                'book_id': self.DEFAULT_CASH_BOOK_ID['id'],
                'metadata_filter': {'order_id': order_id}
            }
        ])

        if block_book_order_balances == {}:
            raise Exception(ErrorCodes.INSUFFICIENT_FUNDS.value)

        from_currency_balance = cash_book_order_balances.get(from_currency, "0")
        to_currency_balance = main_book_order_balances.get(to_currency, "0")

        if Decimal(to_amount) <= Decimal(to_currency_balance) or Decimal(from_amount) <= Decimal(from_currency_balance):
            raise Exception(ErrorCodes.FILL_REQUEST_SEQUENCE_ERROR.value)

        delta_from_amount = str(Decimal(from_amount) - Decimal(from_currency_balance))
        delta_to_amount = str(Decimal(to_amount) - Decimal(to_currency_balance))

        if Decimal(delta_from_amount) > Decimal(block_book_order_balances.get(from_currency, "0")):
            raise Exception(ErrorCodes.INSUFFICIENT_FUNDS.value)

        metadata['order_id'] = order_id
        metadata['order_type'] = order_type
        metadata['type'] = 'FILL'
        metadata['operation'] = 'ORDER'

        entries = [
            {
                "bookId": self.bank_account['ledger_books']['main_balance']['id'],
                "assetId": to_currency,
                "value": delta_to_amount
            },
            {
                "bookId": self.bank_account['ledger_books']['blocked_balance']['id'],
                "assetId": from_currency,
                "value": str(Decimal(delta_from_amount) * Decimal("-1"))
            },
            {
                "bookId": self.DEFAULT_CASH_BOOK_ID['id'],
                "assetId": from_currency,
                "value": delta_from_amount
            },
            {
                "bookId": self.DEFAULT_CASH_BOOK_ID['id'],
                "assetId": to_currency,
                "value": str(Decimal(delta_to_amount) * Decimal("-1"))
            }
        ]

        operation = self.ledger.post_operation(OperationType.CUSTOM, entries, memo, metadata)
        log.info(operation)
        return operation

    def get_order_fill_status_in_bulk(self, order_id_list: list):
        log.info("---------get_Limit_order_fill_status_in_bulk----------")
        bulk_order_fill_status = []

        main_balance_order_query = []
        for order_id in order_id_list:
            main_balance_order_query.append(
                {'book_id':self.bank_account['ledger_books']['main_balance']['id'], 'metadata_filter' : {'order_id':order_id}}
            )
        main_balance_order_query_response = self.get_book_balances_bulk(main_balance_order_query)

        cashbook_balance_order_query = []
        for order_id in order_id_list:
            cashbook_balance_order_query.append(
                {'book_id': self.DEFAULT_CASH_BOOK_ID['id'], 'metadata_filter': {'order_id': order_id}}
            )
        cashbook_balance_order_query_response = self.get_book_balances_bulk(cashbook_balance_order_query)

        if not (len(cashbook_balance_order_query_response) == len(order_id_list) and len(main_balance_order_query_response) == len(order_id_list)):
            raise Exception(ErrorCodes.FETCH_ORDER_STATUS_ERROR.value)

        for counter in range(len(order_id_list)):
            order_wise_fill_status = {}
            order_wise_fill_status['fill_status'] = {}
            order_wise_fill_status['order_id'] = order_id_list[counter]
            for (key,val) in main_balance_order_query_response[counter].items():
                if Decimal(val)>0:
                    order_wise_fill_status['fill_status']['to_currency'] = key
                    order_wise_fill_status['fill_status']['to_amount'] = val
                    break
            for (key,val) in cashbook_balance_order_query_response[counter].items():
                if Decimal(val)>0:
                    order_wise_fill_status['fill_status']['from_currency'] = key
                    order_wise_fill_status['fill_status']['from_amount'] = val
                    break
            bulk_order_fill_status.append(order_wise_fill_status)

        return bulk_order_fill_status

