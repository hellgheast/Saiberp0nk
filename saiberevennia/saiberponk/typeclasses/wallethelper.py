class WalletHelper:

    def __init__(self, character) -> None:
        self.character = character
        self.character.db.wallet = 0

    @property
    def content(self):
        return self.character.db.wallet
    
    def setup(self):
        self.character.db.wallet = 0

    def increment(self,amount:int):
        self.character.db.wallet += amount

    def decrement(self,amount:int):
        self.character.db.wallet -= amount
    