class Pif:
    def __init__(self):
        self.pif = []
    
    def add(self, token, pos):
        self.pif.append((token, pos))

    def __str__(self):
        return "\n".join(f"Token: {token}  Position: {pos}" for token, pos in self.pif)