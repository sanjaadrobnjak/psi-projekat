import random

class RandomSampleMixin:
    @classmethod
    def sample(cls, k, *, counts=None):
        objs = list(cls.objects.all())
        return random.sample(objs, k, counts=counts)
