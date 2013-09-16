from datetime import datetime

from django.conf import settings

from pycoin.wallet import Wallet

def calculateMonth(date):
    result = date.month + (date.year * 12) - settings.DONATIONS_LAUNCH_MONTH
    if result < 0:
        raise ValueError( "Too early date: the donations issuance program was launched after that." )
    return result

def calculateSubKey(master_wallet, date, org_id):
    return master_wallet.subkey_for_path('%s/%s' % calculateMonth(date), org_id)

def calculateMonthSubKey(master_wallet, date):
    return master_wallet.subkey_for_path('%s' % calculateMonth(date))

def calculateSubKeyFast(master_month_wallet, org_id):
    return master_month_wallet.subkey_for_path('%s' % org_id)

def donationsSubKey():
    return Wallet.from_wallet_key(settings.DONATIONS_WALLET_KEY)

def donationsOrgSubKey(date, org_id):
    return calculateSubKey(donationsSubKey(), date, org_id)

def donationsMonthSubKey(date):
    return calculateMonthSubKey(donationsSubKey(), date)

SUBKEY_CURRENT_MONTH = donationsMonthSubKey(datetime.now())

def donationsCurrentSubKeyFast(org_id):
    return SUBKEY_CURRENT_MONTH.subkey_for_path('%s' % org_id)
