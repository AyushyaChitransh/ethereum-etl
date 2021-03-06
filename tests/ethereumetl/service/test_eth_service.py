# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os

import pytest
from dateutil.parser import parse
from web3 import HTTPProvider, Web3

from ethereumetl.service.eth_service import EthService
from ethereumetl.service.graph_operations import OutOfBoundsError

run_slow_tests = os.environ.get('ETHEREUM_ETL_RUN_SLOW_TESTS', None) == '1'
skip_slow_tests = pytest.mark.skipif(not run_slow_tests, reason='Slow running tests')


@skip_slow_tests
@pytest.mark.parametrize("date,expected_start_block,expected_end_block", [
    ('2015-07-30', 0, 6911),
    ('2015-07-31', 6912, 13774),
    ('2017-01-01', 2912407, 2918517),
    ('2017-01-02', 2918518, 2924575),
    ('2018-06-10', 5761663, 5767303)
])
def test_get_block_range_for_date(date, expected_start_block, expected_end_block):
    eth_service = get_new_eth_service()
    parsed_date = parse(date)
    blocks = eth_service.get_block_range_for_date(parsed_date)
    assert blocks == (expected_start_block, expected_end_block)


@skip_slow_tests
@pytest.mark.parametrize("date", [
    '2015-07-29',
    '2030-01-01'
])
def test_get_block_range_for_date_fail(date):
    eth_service = get_new_eth_service()
    parsed_date = parse(date)
    with pytest.raises(OutOfBoundsError):
        eth_service.get_block_range_for_date(parsed_date)


@skip_slow_tests
@pytest.mark.parametrize("start_timestamp,end_timestamp,expected_start_block,expected_end_block", [
    (1438270128, 1438270128, 10, 10),
    (1438270128, 1438270129, 10, 10)
])
def test_get_block_range_for_timestamps(start_timestamp, end_timestamp, expected_start_block, expected_end_block):
    eth_service = get_new_eth_service()
    blocks = eth_service.get_block_range_for_timestamps(start_timestamp, end_timestamp)
    assert blocks == (expected_start_block, expected_end_block)


@skip_slow_tests
@pytest.mark.parametrize("start_timestamp,end_timestamp", [
    (1438270129, 1438270131)
])
def test_get_block_range_for_timestamps_fail(start_timestamp, end_timestamp):
    eth_service = get_new_eth_service()
    with pytest.raises(ValueError):
        eth_service.get_block_range_for_timestamps(start_timestamp, end_timestamp)


def get_new_eth_service():
    web3 = Web3(HTTPProvider('https://mainnet.infura.io/'))
    return EthService(web3)
