import pytest
from insnail_ai_tools.mdb import MdbInsertUtil

mdb_insert_util = MdbInsertUtil("http://172.18.23.31:8002")
test_data = [{"str1": "abc", "str2": "", "int1": 10, "int2": 0}]


def test_report_batch_data():
    result = mdb_insert_util.report_batch_data("table_test", test_data)
    assert result["msg"] == "success"


@pytest.mark.asyncio
async def test_report_batch_data_async():
    result = await mdb_insert_util.report_batch_data_async("table_test", test_data)
    assert result["msg"] == "success"
