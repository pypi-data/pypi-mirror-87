import logging
import requests
import aiohttp
from urllib.parse import urljoin
from typing import List


class MdbInsertUtil:
    """
    example:
    >>> mdb_insert_util = MdbInsertUtil(base_url="")
    >>> mdb_insert_util.report_batch_data("test_table", [])
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.batch_report_url = urljoin(self.base_url, "batch_report_data")

    def report_batch_data(
        self, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        body = self._get_report_body(table, data_list, mode)
        rp = requests.post(self.batch_report_url, json=body)
        result = rp.json()
        logging.info(f"post data to mdb, status [{result['msg']}]")
        return result

    async def report_batch_data_async(
        self, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        body = self._get_report_body(table, data_list, mode)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.batch_report_url, json=body) as response:
                result = await response.json()
                logging.info(f"post data to mdb, status [{result['msg']}]")
                return result

    @classmethod
    def _get_report_body(
        cls, table: str, data_list: List[dict], mode: str = None
    ) -> dict:
        _data_list = []
        for data in data_list:
            d = dict()
            for k, v in data.items():
                if v is not None:
                    d[k] = v
            _data_list.append(d)
        body = {"table": table, "data_list": _data_list}
        if mode:
            body["mode"] = mode
        return body
