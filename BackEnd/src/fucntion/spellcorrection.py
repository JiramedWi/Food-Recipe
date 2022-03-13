from spellchecker import SpellChecker

dict = '../../resource/mergedict.txt'
spell = SpellChecker(language='en')
spell.word_frequency.load_text_file(dict)


def spell_corr(query):
    spellcor = [spell.correction(w) for w in query.split()]
    return spellcor
