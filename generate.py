from vendor.passphrase.passphrase import Passphrase
from vendor.skydb import skydb
import os
import stat

def generate_seed():
    passphrase = Passphrase('internal')
    passphrase.amount_w = 18
    passphrase.amount_n = 0
    return ' '.join(passphrase.generate())

if __name__ == '__main__':
    portal = input('What is your preferred Skynet portal? [ https://siasky.net/ ] > ')
    if portal == '':
        portal = 'https://siasky.net/'

    label = input('What would you like to name this beacon? [ Unnamed Entropy Beacon ] > ')
    if label == '':
        label = 'Unnamed Entropy Beacon'

    with open('config.py', 'w') as f:
        f.write('portal = "{0}"'.format(portal))

    print('Your configuration settings have been saved to config.py.')

    # Generating seed and using seed to generate public key. Seed and public key
    # are saved to files. There is no need to persist the secret key since it is
    # generated with the seed.

    seed = generate_seed()
    pk, sk = skydb.crypto.genKeyPairFromSeed(seed)

    entry = skydb.RegistryEntry(pk, sk)
    entry.set_entry(data_key='entropybeacon:label', data=label, revision=0)

    with open('skynet_ed25519.seed', 'w') as f:
        f.write(seed)

    os.chmod('skynet_ed25519.seed', stat.S_IRUSR)

    with open('skynet_ed25519.pub', 'w') as f:
        f.write(pk.hex())

    print('Your seed has been saved to skynet_ed25519.seed. Keep this safe. Do not share it with anyone.')

    print('Your public key has been skynet_ed25519.pub. This public key identifies you / your server as the source of the data. The key is as follows:')
    print(pk.hex())
