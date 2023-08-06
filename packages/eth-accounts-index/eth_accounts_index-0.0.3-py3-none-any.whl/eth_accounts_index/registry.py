import logging
import json
import os

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


class AccountRegistry:

    __abi = None
    __bytecode = None

    def __init__(self, w3, address, signer_address=None):
        abi = AccountRegistry.abi()
        AccountRegistry.bytecode()
        self.contract = w3.eth.contract(abi=abi, address=address)
        self.w3 = w3
        if signer_address != None:
            self.signer_address = signer_address
        else:
            if type(self.w3.eth.defaultAccount).__name__ == 'Empty':
                self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
            self.signer_address = self.w3.eth.defaultAccount


    @staticmethod
    def abi():
        if AccountRegistry.__abi == None:
            f = open(os.path.join(datadir, 'registry.abi.json'), 'r')
            AccountRegistry.__abi = json.load(f)
            f.close()
        return AccountRegistry.__abi


    @staticmethod
    def bytecode():
        if AccountRegistry.__bytecode == None:
            f = open(os.path.join(datadir, 'registry.bin'))
            AccountRegistry.__bytecode = f.read()
            f.close()
        return AccountRegistry.__bytecode


    def add(self, address):
        gasPrice = self.w3.eth.gasPrice;
        nonce = self.w3.eth.getTransactionCount(self.signer_address, 'pending')
        tx = self.contract.functions.add(address).buildTransaction({
            'gasPrice': gasPrice,
            'gas': 100000,
            'from': self.signer_address,
            'nonce': nonce,
            })
        logg.debug('tx {}'.format(tx))
        tx_hash = self.contract.functions.add(address).transact({
            'gasPrice': gasPrice,
            'gas': 100000,
            'from': self.signer_address,
            'nonce': nonce,
            })
        return tx_hash


    def count(self):
        return self.contract.functions.count().call()


    def have(self, address):
        r = self.contract.functions.accountsIndex(address).call()
        return r != 0


    def last(self, n):
        c = self.count()
        lo = c - n - 1
        if lo < 0:
            lo = 0
        accounts = []
        for i in range(c - 1, lo, -1):
            a = self.contract.functions.accounts(i).call()
            accounts.append(a)
        return accounts
