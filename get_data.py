import nltk

corpora = [
            'gutenberg',
            'punkt',
            'averaged_perceptron_tagger',
        ]

if __name__ == "__main__":
    for cr in corpora:
        nltk.download(cr)
