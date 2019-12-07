def poscode2word(pos):
    tag_des = {
        'CC': 'Coordinating conjunction',
        'CD': 'Cardinal number',
        'DT': 'Determiner',
        'EX': 'Existential',
        'FW': 'Foreign word',
        'IN': 'Preposition',
        'JJ': 'Adjective',
        'JJR': 'Adjective, comparative',
        'JJS': 'Adjective, superlative',
        'LS': 'List item maker',
        'MD': 'Modal',
        'NN': 'Noun, sigular',
        'NNS': 'Noun, plural',
        'NNP': 'Proper noun, singular',
        'NNPS': 'Proper noun, plural',
        'PDT': 'Predeterminer',
        'POS': 'Possessive ending',
        'PRP': 'Personal pronoun',
        'PRP$': 'Possessive pronoun',
        'RB': 'Adverb',
        'RBR': 'Adverb, comparative',
        'RBS': 'Adverb, superlative',
        'RP': 'Particle',
        'SYM': 'Symbol',
        'TO': 'to',
        'UH': 'Interjection',
        'VB': 'Verb, base form',
        'VBD': 'Verb, past tense',
        'VBG': 'Verb, gerund or present participle',
        'VBP': 'Verb, non-3rd person singular present',
        'VBZ': 'Verb, 3rd person singular present',
        'WDT': 'Wh-determiner',
        'WP': 'Wh-pronoun',
        'WP$': 'Possessive wh-pronoun',
        'WRB': 'Wh-adverb'
    }

    if pos in tag_des:
        return tag_des[pos]
    return pos

if __name__ == "__main__":
    print(poscode2word('NN'))
