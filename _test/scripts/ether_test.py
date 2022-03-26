ETHERSCAN_API_KEY = "31R4F4TFA8WDXNXQ6F7XE9Z31B9TR749Q9"
from etherscan import Etherscan
import pathlib
from pprint import pformat, pprint
import json
eth = Etherscan(ETHERSCAN_API_KEY)
#balance = eth.get_eth_balance(address="0xE5d4924413ae59AE717358526bbe11BB4A5D76b9")
#print(int(balance) / 1e18)
azuki_contract_address = "0xED5AF388653567Af2F388E6224dC7C4b3241C544"
azuki_contract_code = eth.get_contract_source_code(azuki_contract_address)[0]

root_dir = pathlib.Path("azuki")
root_dir.mkdir(parents=True, exist_ok=True)

for k, v in azuki_contract_code.items():
    if k in ("ABI"):
        v = json.loads(v)
        v = json.dumps(v, indent=4)
    if k in ("SourceCode"):
        v = json.loads(v[1:-1])
        v = json.dumps(v, indent=4)
    with open(str(root_dir / f"{k}.sol"), "w") as f:
        #f.write(json.dumps(_, indent=4)
        f.write(v)