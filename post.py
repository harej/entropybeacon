from vendor.skydb import skydb
from time import sleep
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
    randomness = os.urandom(56).hex()
    timestamp = int(arrow.utcnow().timestamp())

    entry = skydb.RegistryEntry(pk, sk)
    entry.set_entry(data_key='entropybeacon:data', data=randomness, revision=timestamp)

    try:
        randomness, data_revision = entry.get_entry(data_key='entropybeacon:data')
    except:
        print('While checking if the update succeeded, the randomness data retrieval failed.')
        raise

    return {'public_key': 'ed25519:' + pk.hex(),
            'randomness': randomness,
            'revision': timestamp}

if __name__ == '__main__':
    print(json.dumps(update()))
    sleep(30)
    print(json.dumps(update()))
