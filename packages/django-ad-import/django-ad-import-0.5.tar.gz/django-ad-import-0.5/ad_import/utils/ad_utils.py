"""
 * Convert a microsoft timestamp to UNIX timestamp
 * http://www.morecavalier.com/index.php?whom=Apps%2FLDAP+timestamp+converter
 * @param int ad_date Microsoft timestamp
 * @return int UNIX timestamp
 """
from datetime import datetime


def microsoft_timestamp_to_unix(ad_date):
    ad_date = int(ad_date)
    if not ad_date:
        raise ValueError('Invalid date')

    secsAfterADEpoch = ad_date / 10000000
    AD2Unix = ((1970 - 1601) * 365 - 3 + round((1970 - 1601) / 4)) * 86400

    """Why -3 ?
    If the year is the last year of a century, eg. 1700, 1800, 1900, 2000,
    then it is only a leap year if it is exactly divisible by 400.
    Therefore, 1900 wasn't a leap year but 2000 was."""

    unixTimeStamp = int(secsAfterADEpoch - AD2Unix)

    return unixTimeStamp


def parse_date(ad_timestamp) -> datetime:
    timestamp = microsoft_timestamp_to_unix(ad_timestamp)
    return datetime.fromtimestamp(timestamp)


def find_flags(flag):
    flag_list = {
        1: 'SCRIPT',
        2: 'ACCOUNTDISABLE',
        8: 'HOMEDIR_REQUIRED',
        16: 'LOCKOUT',
        32: 'PASSWD_NOTREQD',
        64: 'PASSWD_CANT_CHANGE',
        128: 'ENCRYPTED_TEXT_PWD_ALLOWED',
        256: 'TEMP_DUPLICATE_ACCOUNT',
        512: 'NORMAL_ACCOUNT',
        2048: 'INTERDOMAIN_TRUST_ACCOUNT',
        4096: 'WORKSTATION_TRUST_ACCOUNT',
        8192: 'SERVER_TRUST_ACCOUNT',
        65536: 'DONT_EXPIRE_PASSWORD',
        131072: 'MNS_LOGON_ACCOUNT',
        262144: 'SMARTCARD_REQUIRED',
        524288: 'TRUSTED_FOR_DELEGATION',
        1048576: 'NOT_DELEGATED',
        2097152: 'USE_DES_KEY_ONLY',
        4194304: 'DONT_REQ_PREAUTH',
        8388608: 'PASSWORD_EXPIRED',
        16777216: 'TRUSTED_TO_AUTH_FOR_DELEGATION',
        67108864: 'PARTIAL_SECRETS_ACCOUNT'
    }
    flags = []
    for i in range(0, 27):

        if flag & (1 << i):
            flags.append(1 << i)

    flags_output = {}
    for v in flags:
        flags_output[v] = flag_list[v]

    return flags_output
