import pytest
import itertools
import requests

from brownie import Contract

ALL_PAIRS =[
    ["0xC4dAf3b5e2A9e93861c3FBDd25f1e943B8D87417", "0x84E13785B5a27879921D6F685f041421C7F482dA", [(False, "0x42d7025938bEc20B69cBae5A77421082407f053A", 1)]], # META to 3CRV
    ["0x84E13785B5a27879921D6F685f041421C7F482dA", "0xC4dAf3b5e2A9e93861c3FBDd25f1e943B8D87417",  [(True, "0x42d7025938bEc20B69cBae5A77421082407f053A", 1)]], # 3CRV to META
    ["0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9", "0xC4dAf3b5e2A9e93861c3FBDd25f1e943B8D87417", [(True, "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", 1), (True, "0x42d7025938bEc20B69cBae5A77421082407f053A", 1)]] # USDC vault to cuve vault
    ["0xC4dAf3b5e2A9e93861c3FBDd25f1e943B8D87417", "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9", [(False, "0x42d7025938bEc20B69cBae5A77421082407f053A", 1), (False, "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", 1)]] # USDC vault to cuve vault

    # metapool to tri pool
]

@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def user(accounts):
    yield accounts[1]


@pytest.fixture(params=ALL_PAIRS)
def vaults(request):
    yield request.param


@pytest.fixture()
def vault_from(vaults):
    yield Contract(vaults[0])


@pytest.fixture()
def vault_to(vaults):
    yield Contract(vaults[1])

@pytest.fixture()
def instructions(vaults):
    yield vaults[2]

@pytest.fixture
def whale(vault_from):
    url = "https://api.ethplorer.io/getTopTokenHolders/" + vault_from.address + "?apiKey=freekey"
    resp = requests.get(url, allow_redirects=True)
    yield resp.json()["holders"][0]["address"]


@pytest.fixture
def amount(vault_from):
    if (
        vault_from.address == "0x1C6a9783F812b3Af3aBbf7de64c3cD7CC7D1af44"
        or "USD" in vault_from.name()
    ):
        yield 1000 * 10 ** vault_from.decimals()  # 1000 USD
    else:
        yield 0.1 * 10 ** vault_from.decimals()  # 0.1 BTC


@pytest.fixture
def vault_swapper(gov, CrvVaultSwapper):
    yield gov.deploy(CrvVaultSwapper)


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass