from measurement.pav import PAV
from measurement.sav import SAV


def measure(word1, word2):
    """
    combine phonetic association value and semantic association value

    @word1 -- the first word
    @word2 -- the second word
    @return -- a combined metric value to determine how associated these two words are
    """
    # contribution parameter of phonetic association value
    ALPHA = 0.68

    pa_v = PAV(word1, word2)
    sa_v = SAV(word1, word2)
    if pa_v is None or sa_v is None:
        return 0

    return ALPHA * pa_v + (1 - ALPHA) * sa_v