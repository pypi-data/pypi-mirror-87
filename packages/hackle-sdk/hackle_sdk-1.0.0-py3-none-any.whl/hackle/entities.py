import abc

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class BaseExperiment(ABC):
    def __init__(self, id, key):
        self.id = id
        self.key = key


class RunningExperiment(BaseExperiment):
    def __init__(self, id, key, bucket, variations, execution, **kwargs):
        super(RunningExperiment, self).__init__(id, key)
        self.bucket = bucket
        self.variations = variations
        user_overrides = {}
        for userOverride in execution['userOverrides']:
            user_overrides[userOverride['userId']] = self.variations.get(userOverride['variationId'])
        self.userOverrides = user_overrides

    def __repr__(self):
        return '(id={}, key={}, bucket={}, variations={}, userOverrides={})'.format(self.id, self.key,
                                                                                    self.bucket, self.variations,
                                                                                    self.userOverrides)


class CompletedExperiment(BaseExperiment):
    def __init__(self, id, key, winner_variation_key):
        super(CompletedExperiment, self).__init__(id, key)
        self.winnerVariationKey = winner_variation_key


class Variation(object):
    def __init__(self, id, key, is_dropped, **kwargs):
        self.id = id
        self.key = key
        self.isDropped = is_dropped


class UserOverride(object):
    def __init__(self, user_id, variation, **kwargs):
        self.userId = user_id,
        self.variation = variation


class Bucket(object):
    def __init__(self, seed, slot_size, slots, **kwargs):
        self.seed = seed
        self.slotSize = slot_size
        self.slots = slots


class Slot(object):
    def __init__(self, start_inclusive, end_exclusive, variation_id, **kwargs):
        self.startInclusive = start_inclusive
        self.endExclusive = end_exclusive
        self.variationId = variation_id

    def contains(self, slot_number):
        return (self.startInclusive <= slot_number) and (slot_number < self.endExclusive)


class Event(object):
    def __init__(self, id, key):
        self.id = id
        self.key = key
