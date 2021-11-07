from src.parsing import discord


def run():
    _test_tokenize_bad_input()
    _test_words()
    _test_punctuation()
    _test_url()
    _test_mention()
    _test_emoji()
    _test_mixed()
    print('All tokenizer tests passed.')

def _test_tokenize_bad_input():
    tokenizer = discord.ChatTokenizer()
    try:
        next(tokenizer.tokenize(''))
        assert False
    except TypeError as _: assert True
    try:
        next(tokenizer.tokenize([]))
        assert False
    except TypeError as _: assert True
    try:
        next(tokenizer.tokenize(None))
        assert False
    except TypeError as _: assert True

def _test_words():
    tokenizer = discord.ChatTokenizer()

    message = 'When zombies arrive quickly fax judge Pat'
    tokens  = list(tokenizer.tokenize(message))
    assert [token.type for token in tokens] == [discord.TokenType.WORD] * 7

    message = f'When zombies arrive, quickly fax judge Pat.'
    tokens  = list(tokenizer.tokenize(message))
    assert not all(token.type == discord.TokenType.WORD for token in tokens)
    assert len([token.type for token in tokens if token.type == discord.TokenType.WORD]) == 7
    
    message = f'Wh!en zomb*ve, qui.ckly f"a"x ju,dge P:at.'
    tokens  = list(tokenizer.tokenize(message))
    assert len([token.type for token in tokens if token.type == discord.TokenType.WORD]) == 13

def _test_punctuation():
    tokenizer = discord.ChatTokenizer()

    message = '.,!?:*^'
    tokens = list(tokenizer.tokenize(message))
    assert [token.type for token in tokens] == [discord.TokenType.PUNCTUATION] * 7

    message = f'When zombies arrive, quickly fax judge Pat.'
    tokens  = list(tokenizer.tokenize(message))
    assert not all(token.type == discord.TokenType.PUNCTUATION for token in tokens)
    assert len([token.type for token in tokens if token.type == discord.TokenType.PUNCTUATION]) == 2

    message = f'Wh!en zomb*ve, qui.ckly f"a"x ju,dge P:at.'
    tokens = list(tokenizer.tokenize(message))
    assert len([token.type for token in tokens if token.type == discord.TokenType.PUNCTUATION]) == 9

def _test_url():
    tokenizer = discord.ChatTokenizer()

    URLs = [ 
        'https://xyz.com',
        'https://xyz.io',
        'http://xyz.com',
        'http://xyz.io',
        'http://\9893838833__@#89838'
    ]
    tokens = [token.type for url in URLs for token in tokenizer.tokenize(url)]
    assert tokens == [discord.TokenType.URL] * len(URLs)

    # Note, the tokenizer works on intent; it doesn't care if the URL is malformed,
    # it only looks for the prefix http(s)://
    NotURLs = [
        'www.xyz.com',
        'xyz.io',
        'ht?tps://xyz.io',
    ]
    tokens = [token for notURL in NotURLs 
                     for token in tokenizer.tokenize(notURL)]
    assert not any(token.type == discord.TokenType.URL for token in tokens)


def _test_mention():
    tokenizer = discord.ChatTokenizer()
    message = '<@!123456789> <@2345678910>'
    assert [token.type == discord.TokenType.MENTION for token in tokenizer.tokenize(message)]

def _test_emoji():
    tokenizer = discord.ChatTokenizer()
    message = '<:EMOJI_NAME:12345> <@:EMOJI_NAME:12345>'
    assert [token.type == discord.TokenType.EMOJI for token in tokenizer.tokenize(message)]
    

def _test_mixed():
    tokenizer = discord.ChatTokenizer() 
    message = '<@!123456789> <@2345678910> Hey, want to play? <:EMOJI_NAME:12345> Sign up at https://____.com!'
    types = [token.type for token in tokenizer.tokenize(message)]
    assert types == [
        discord.TokenType.MENTION, 
        discord.TokenType.MENTION, 
        discord.TokenType.WORD, 
        discord.TokenType.PUNCTUATION,
        discord.TokenType.WORD,
        discord.TokenType.WORD,
        discord.TokenType.WORD,
        discord.TokenType.PUNCTUATION,
        discord.TokenType.EMOJI,
        discord.TokenType.WORD,
        discord.TokenType.WORD,
        discord.TokenType.WORD,
        discord.TokenType.URL
    ]



def _pprint_tokens(tokens):
    for token in tokens:
        print()
        print(token.instance)
        print(token.type.name)
