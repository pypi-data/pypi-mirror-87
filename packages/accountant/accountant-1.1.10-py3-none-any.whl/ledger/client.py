import time
from enum import auto
from typing import List

from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.requests import Request

import logging

from jsonrpcclient.exceptions import ReceivedNon2xxResponseError

from common.cs_enum import AutoName

DEFAULT_LEDGER_BOOK_ID = "1"

log = logging.getLogger(__name__)


class OperationType(AutoName):
    TRANSFER = auto()
    CUSTOM = auto()
    VOID = auto()


class OperationStatus(AutoName):
    INIT = auto()
    PROCESSING = auto()
    APPLIED = auto()
    REJECTED = auto()


class LedgerClient:
    def __init__(self, ledger_endpoint: str, ledger_read_only_endpoint: str = None):
        self.rpc_client = HTTPClient(ledger_endpoint)
        if ledger_read_only_endpoint is not None:
            self.read_only_rpc_client = HTTPClient(ledger_read_only_endpoint)

    def _execute(self, method: str, *args, read_only_method: bool = False, retry_index=0):
        start_time = int(time.time()*1000)
        try:
            if read_only_method is True and getattr(self, "read_only_rpc_client", None) is not None:
                rpc_response = self.read_only_rpc_client.request(method, *args)
            else:
                rpc_response = self.rpc_client.request(method, *args)
        except ReceivedNon2xxResponseError as e:
            if e.code == 502 and retry_index <= 3:
                log.warning(f"Retrying 502 response", exc_info=1)
                return self._execute(method, *args, read_only_method=read_only_method, retry_index=retry_index+1)
            raise e
        end_time = int(time.time()*1000)
        log.info(f"LedgerClient: {method}: time_taken: {end_time-start_time}ms")
        return rpc_response.data.result

    def _bulk_execute(self,request_list: List, read_only_method: bool = False, retry_index=0):
        start_time = int(time.time()*1000)
        try:
            if read_only_method is True and getattr(self, "read_only_rpc_client", None) is not None:
                rpc_response = self.read_only_rpc_client.send(request_list)
            else:
                rpc_response = self.rpc_client.send(request_list)
        except ReceivedNon2xxResponseError as e:
            if e.code == 502 and retry_index <= 3:
                log.warning(f"Retrying 502 response", exc_info=1)
                return self._bulk_execute(request_list, read_only_method=read_only_method, retry_index=retry_index+1)
            raise e
        end_time = int(time.time()*1000)
        log.info(f"LedgerClient: time_taken: {end_time-start_time}ms")
        result = []
        res_id_map = {}
        for each_response in rpc_response.data:
            res_id_map[each_response.id] = each_response.result
        for each_request in request_list:
            result.append(res_id_map[each_request['id']])
        return result

    def create_book(self, name: str, min_balance: str = None, metadata: dict = None):
        book_info = dict()
        book_info["name"] = name
        book_info["metadata"] = metadata
        if min_balance:
            book_info["restrictions"] = dict()
            book_info["restrictions"]["minBalance"] = min_balance
        return self._execute("createBook", book_info)

    def get_book(self, book_id: str, timestamp: int = None):
        filter = {"toTime": timestamp} if timestamp else None
        return self._execute("getBook", book_id, filter, read_only_method=True)

    def put_book(self, book_id: str, restrictions: dict):
        return self._execute("putBook", book_id, restrictions)

    def freeze_book(self, book_id: str):
        return self.put_book(book_id=book_id, restrictions={"freeze": True})

    def unfreeze_book(self, book_id: str):
        return self.put_book(book_id=book_id, restrictions={"freeze": False})

    def get_book_balances(self, book_id: str, asset_id: str = None, metadata_filter: dict = None, timestamp: int = None):
        filter = {"toTime": timestamp} if timestamp else None
        return self._execute("getBalances", book_id, asset_id, metadata_filter, filter, read_only_method=True)

    def get_book_balances_bulk(self, params_list: list = []):
        request_list = []
        for params in params_list:
            if not params.get('book_id'):
                raise Exception('invalid input to get_book_balances_bulk: book_id missing')
            params['asset_id'] = params.get('asset_id',None)
            params['metadata_filter'] = params.get('metadata_filter', None)
            params['filter'] = {"toTime": params['timestamp']} if params.get('timestamp', None) else None
            request_list.append(
                Request("getBalances", params['book_id'], params['asset_id'], params['metadata_filter'], params['filter'])
            )
        return self._bulk_execute(request_list, read_only_method = True)

    def get_operation(self, operation_id: str):
        return self._execute("getOperation", operation_id, read_only_method=True)

    def get_operations(self, book_id: str, metadata_filter: dict = None):
        return self._execute("getOperations", book_id, metadata_filter, read_only_method=True)

    def post_operation(self, operation_type: OperationType, entries: List[dict], memo: str = "", metadata: dict = None):
        operation = dict()
        operation["type"] = operation_type.value
        operation["entries"] = entries
        operation["memo"] = memo
        if metadata: operation["metadata"] = metadata
        result = self._execute("postOperation", operation)
        if result["status"] == OperationStatus.REJECTED.value:
            raise Exception(result["rejectionReason"])
        return result

    def post_transfer(self, from_book_id: str, to_book_id: str, asset_id: str, value: str, memo: str = "", metadata: dict = None):
        transfer = dict()
        transfer["fromBookId"] = from_book_id
        transfer["toBookId"] = to_book_id
        transfer["assetId"] = asset_id
        transfer["value"] = value
        transfer["memo"] = memo
        if metadata: transfer["metadata"] = metadata
        result = self._execute("postTransfer", transfer)
        if result["status"] == OperationStatus.REJECTED.value:
            raise Exception(result["rejectionReason"])
        return result

    def get_diff(self, from_time: int, to_time: int):
        return self._execute("getDiff", from_time, to_time, read_only_method=True)

    def post_void(self, operation_id_list: list, memo: str, metadata: dict = None):
        void = dict()
        void["operationIds"] = operation_id_list
        void["memo"] = memo
        void["metadata"] = metadata or {}
        result = self._execute("postVoid", void)
        if result["status"] == OperationStatus.REJECTED.value:
            raise Exception(result["rejectionReason"])
        return result
