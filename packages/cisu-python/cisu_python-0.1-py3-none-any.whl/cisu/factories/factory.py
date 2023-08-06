from .seeds import faker, clock_seed, location_seed

class Factory:
    def __init__(self):
        self.faker = faker
        self.clock_seed = clock_seed
        self.location_seed = location_seed
