from datetime import datetime

from django.conf import settings

from pycoin.wallet import Wallet

# The first derivation is for the month
# Not used anymore, is always month 0 (more practical)
SUBKEY_ALL_MONTHS = Wallet.from_wallet_key(settings.DONATIONS_WALLET_KEY).subkey_for_path('0')

def donationsOrgSubKey(org_id):
    return SUBKEY_ALL_MONTHS.subkey_for_path('%d' % org_id)

def donationsOrgAddress(org_id):
    return SUBKEY_ALL_MONTHS.subkey_for_path('%d' % org_id).bitcoin_address()
