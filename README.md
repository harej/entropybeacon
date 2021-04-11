The Skynet Entropy Beacon provides securely generated randomness, produced by the beacon of your choice, delivered through the decentralized content network Skynet.

Lightweight beacons that anyone can run post random data on Skynet approximately once every 30 seconds, and this randomness can be used if you do not trust your user or device to provide genuinely random data. Each random data beacon is identified by its public key, and this public key can be used to verify the signature associated with the random data, so you can be sure that the data comes from the source it claims to come from.

The beacons also upload a timestamp at approximately the same time they upload the random data. This is meant to give an idea as to how fresh the data is. Entropy Beacon is not designed to be used as a timestamping service.

## Set up your own beacon

1. `git clone https://github.com/harej/entropybeacon && cd entropybeacon`
2. `git submodule init && git submodule update`
3. Install python3, python3-pip, and testresources if you have not yet.
4. `pip3 install -r requirements.txt`
5. `pip3 install -r vendor/skydb/requirements.txt`
6. `python3 generate.py`
7. Follow the prompts to generate your public key.
8. Add a crontab entry to run the script every minute, something like this: `* * * * * /usr/bin/python3 /opt/entropybeacon/post.py`
9. To get your new beacon listed on https://entropybeacon.hns.siasky.net, file a GitHub issue with the beacon's public key.

## Set up your own beacon listing

The source code for beacon listings is available at https://github.com/harej/entropybeacon-site
