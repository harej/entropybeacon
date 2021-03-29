from vendor.skydb import skydb
import arrow
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    from config import portal
except ImportError:
    print('\n\nNo config.py found. Did you run generate.py?\n\n')
    raise

seed = None
try:
    with open(os.path.join(__location__, 'skynet_ed25519.seed')) as f:
        seed = f.read()
except:
    print('\n\nSeed file not found. Did you run generate.py?\n\n')
    raise

pk, sk = skydb.crypto.genKeyPairFromSeed(seed)

def update():
    entry = skydb.RegistryEntry(pk, sk)

    # Retrieving current registry values if they exist.

    try:
        old_randomness, data_revision = entry.get_entry(data_key='entropybeacon:data', timeout=5)
    except:
        data_revision = -1
    try:
        old_timestamp, timestamp_revision = entry.get_entry(data_key='entropybeacon:time', timeout=5)
    except:
        timestamp_revision = -1

    # The randomness key and the timestamp key are supposed to both be updated
    # at the same time. If there is a difference, it means there is drift between
    # the two, which effectively means it is corrupt and no longer should be used.

    if data_revision != timestamp_revision:
        print('Data revision is {0} while timestamp revision is {1}. Drift detected, will not continue.'.format(str(data_revision), str(timestamp_revision)))
        raise Exception

    randomness = os.urandom(56).hex()
    timestamp = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss') + 'Z'

    entry.set_entry(data_key='entropybeacon:data', data=randomness, revision=data_revision+1)
    entry.set_entry(data_key='entropybeacon:time', data=timestamp, revision=timestamp_revision+1)

    try:
        randomness, data_revision = entry.get_entry(data_key='entropybeacon:data')
    except:
        print('While checking if the update succeeded, the randomness data retrieval failed.')
        raise
    try:
        timestamp, timestamp_revision = entry.get_entry(data_key='entropybeacon:time')
    except:
        print('While checking if the update succeeded, the timestamp data retrieval failed.')
        raise

    if data_revision != timestamp_revision:
        print('While checking if the update succeeded, drift was detected: data revision is {0} while timestamp revision is {1}. This keypair is no longer usable.'.format(str(data_revision), str(timestamp_revision)))
        raise Exception

    return {'public_key': 'ed25519:' + pk.hex(),
            'randomness': randomness,
            'timestamp': timestamp,
            'revision': data_revision}

if __name__ == '__main__':
    json.dumps(update())

