try:
    import mmh3
except ImportError:
    from .lib import pymmh3 as mmh3


class Bucketer(object):
    def __init__(self):
        return

    def bucketing(self, bucket, user_id):
        slot_number = self._slot_number(user_id, bucket.seed, bucket.slotSize)

        for slot in bucket.slots:
            if slot.contains(slot_number):
                return slot

        return None

    def _slot_number(self, user_id, seed, slot_size):
        hash_value = mmh3.hash(user_id, seed)
        return abs(hash_value) % abs(slot_size)
