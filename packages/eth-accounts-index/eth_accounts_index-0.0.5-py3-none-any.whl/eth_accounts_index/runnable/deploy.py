"""Deploys accounts index, registering arbitrary number of writers

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import os
import json
import argparse
import logging

# third-party imports
import web3


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-w', '--writer', dest='w', action='append', type=str, help='Writer to add')
argparser.add_argument('-a', '--account', dest='a', action='append', type=str, help='Account to add')
argparser.add_argument('-k', '--keep-sender', dest='k', action='store_true', help='If set, sender will be kept as writer')
argparser.add_argument('--contracts-dir', dest='contracts_dir', default='.', help='Directory containing bytecode and abi')
argparser.add_argument('-v', action='store_true', help='Be verbose')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

def main():
    w3 = web3.Web3(web3.Web3.HTTPProvider(args.p))

    f = open(os.path.join(args.contracts_dir, 'AccountsIndex.abi.json'), 'r')
    abi = json.load(f)
    f.close()

    f = open(os.path.join(args.contracts_dir, 'AccountsIndex.bin'), 'r')
    bytecode = f.read()
    f.close()

    w3.eth.defaultAccount = w3.eth.accounts[0]

    c = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = c.constructor().transact({'from': w3.eth.accounts[0]})

    rcpt = w3.eth.getTransactionReceipt(tx_hash)

    address = rcpt.contractAddress
    c = w3.eth.contract(abi=abi, address=address)

    logg.debug('adding sender to write list')
    c.functions.addWriter(w3.eth.accounts[0]).transact()
    
    if args.w != None:
        for w in args.w:
            logg.info('adding {} to write list'.format(w))
            c.functions.addWriter(w).transact()

    if args.a != None:
        for a in args.a:
            logg.info('adding {} to accounts index'.format(a))
            c.functions.add(a).transact()

    if not args.k:
        logg.debug('deleting sender for write list')
        c.functions.deleteWriter(w3.eth.accounts[0]).transact()

    print(address)

#    fail = False
#    try:
#        c.functions.add(w3.eth.accounts[2]).transact({'from': w3.eth.accounts[1]})
#    except:
#        fail = True
#    assert fail
#
#    c.functions.addWriter(w3.eth.accounts[1]).transact({'from': w3.eth.accounts[0]})
#    c.functions.add(w3.eth.accounts[2]).transact({'from': w3.eth.accounts[1]})
#    c.functions.add(w3.eth.accounts[3]).transact({'from': w3.eth.accounts[1]})
#
#    assert c.functions.count().call() == 3
#    assert c.functions.accountsIndex(w3.eth.accounts[3]).call() == 2
#    assert c.functions.accounts(2).call() == w3.eth.accounts[3]
#
#    fail = False
#    try:
#        c.functions.add(w3.eth.accounts[3]).transact({'from': w3.eth.accounts[1]})
#    except:
#        fail = True
#    assert fail


if __name__ == '__main__':
    main()
