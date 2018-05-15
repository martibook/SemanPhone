from .pav import PAV
from .sav import SAV


def measure(word1, word2, ALPHA=0.7):
    """
    combine phonetic association value and semantic association value

    @word1 -- the first word
    @word2 -- the second word
    @ALPHA -- contribution parameter of phonetic association value
    @return -- a combined metric value to determine how associated these two words are
    """
    pa_v = PAV(word1, word2)
    sa_v = SAV(word1, word2)
    if pa_v is None or sa_v is None:
        return 0

    return ALPHA * pa_v + (1 - ALPHA) * sa_v
