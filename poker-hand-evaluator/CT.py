"""card_translate.py"""
import arrays

"""card_translate(rank, suit):
   Translate the card into the evaluator's inner representation and return it.
   rank: (Number) (deuce=0,trey=1,four=2,five=3,...,ace=12)
   suit: (String) 's','h','c','d'
   """
def card_translate(rank, suit):
    suitInt = 0
    if suit == 's':
        suitInt = 1 << 12
    elif suit == 'h':
        suitInt = 2 << 12
    elif suit == 'd':
        suitInt = 4 << 12
    else:
        suitInt = 8 << 12
    prime = ( arrays.primes[rank] |
              rank << 8 |
              suitInt |
              (1 << (16+rank)))
    return prime

if __name__ == '__main__':
    print(card_translate(0,'s')) #2s
    print(card_translate(9,'h')) #Jh
    print(card_translate(3,'d')) #5d
    print(card_translate(12,'c')) #Ac
