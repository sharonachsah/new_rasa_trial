from rasa_gen import NLUTemplate, Generator

if __name__ == '__main__':
    sentence_template = [
        'create board [{}](board_name)[{}]{{"entity":"value","role":"temperature"}}',

    ]
    word_template = [
        'demo',
        'test',
        'test1',
        'test2',
    ]
    template = NLUTemplate().add_sentence(sentence_template=sentence_template)\
                            .add_word(word_template=word_template,mode='new')\
                            .add_random_val(16, 30)
generator = Generator('test_intent').add_template(template)
generator.generate_from_template(50, './test_template.yml')