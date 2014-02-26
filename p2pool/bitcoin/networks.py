import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(
    blackcoin=math.Object(
        P2P_PREFIX='70352205'.decode('hex'),
        P2P_PORT=15714,
        ADDRESS_VERSION=25,
        RPC_PORT=15715,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'blackcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: 10000*100000000,
        BLOCK_PERIOD=60, # s
        SYMBOL='BC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BlackCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BlackCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.blackcoin'), 'blackcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blocks.blackcoin.pw/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blocks.blackcoin.pw/address/',
        TX_EXPLORER_URL_PREFIX='http://blocks.blackcoin.pw/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.01e8,
    ),
    blackcoin_testnet=math.Object(
        P2P_PREFIX='cdf2c0ef'.decode('hex'),
        P2P_PORT=25714,
        ADDRESS_VERSION=111,
        RPC_PORT=25715,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'blackcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: 10000*100000000,
        BLOCK_PERIOD=60, # s
        SYMBOL='BC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BlackCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BlackCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.blackcoin'), 'blackcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://testnet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://testnet/address/',
        TX_EXPLORER_URL_PREFIX='http://testnet/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.01e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
