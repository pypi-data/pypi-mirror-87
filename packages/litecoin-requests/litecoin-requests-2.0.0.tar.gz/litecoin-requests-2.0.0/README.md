Forked from fiatjaf/bitcoin-requests; modified for Litecoin Core

The simplest Litecoin Core RPC library for when you just want to talk to Litecoin Core.

## Usage

If you started Litecoin Core like this:

```bash
litcoind -regtest -rpcuser=user -rpcpassword=pass
```

Instantiate the `litcoin_requests` RPC client like this:

```python
from litcoin_requests import LitcoinRPC

rpc = LitecoinRPC('http://127.0.0.1:9332, 'user', 'pass')
blocks = rpc.generate(101)
tx = rpc.sendtoaddress(address, 20)
```

## Installation

```
pip install litcoin-requests
```
