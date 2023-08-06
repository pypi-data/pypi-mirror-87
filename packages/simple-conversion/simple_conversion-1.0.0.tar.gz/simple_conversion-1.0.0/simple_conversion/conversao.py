class Conversion:
    def __init__(self, val):
        self.val = val

    def mb_into_gb(self):
        return self.val/1024

    def GB_into_MB(self):
        return 1024*self.val

    def GB_into_KB(self):
        return self.val*2**20

    def KB_into_GB(self):
        return self.val/2**20

    def GB_into_bytes(self):
        return self.val*2**30

    def bytes_into_GB(self):
        return self.val/2**30

    def MB_into_bytes(self):
        return self.val*2**20

    def bytes_into_MB(self):
        return self.val/2**20

    def MB_into_KB(self):
        return 1024*self.val

    def KB_into_MB(self):
        return 1024 / self.val

    def KB_into_bytes(self):
        return self.val * 1024

    def bytes_into_KB(self):
        return self.val/1024


