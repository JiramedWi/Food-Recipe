from spellchecker import SpellChecker

spell = SpellChecker(language='en')
spell.word_frequency.load_text_file('../../resource/mergedict.txt')


def spell_corr(query):
    spellcor = [spell.correction(w) for w in query.split()]
    return spellcor
