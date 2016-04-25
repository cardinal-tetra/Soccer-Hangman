# a whole load of helper functions
def produce_hint(answer):
        """make string partially revealing answer where user guessed correctly"""
        hint = []

        for letter in answer:
            if letter[1] == True:
                hint.append(letter[0])
            else:
                hint.append('_ ')

        return ''.join(hint)
