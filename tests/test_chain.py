from src import markov


def run_tests():
    for order in range(1, 10):
        _test_train(order)
        _test_train_bad_input(order)
        _test_generate(order)
        _test_generate_from_seed(order)
        _test_generate_infinite(order)
        _test_generate_from_empty_chain(order)
    print('All Chain tests passed.')

def _test_train(order):
    chain = markov.Chain(order)
    chain.train([1, 2, 3, 4])
    chain.train([5, 6, 7, 8])

def _test_train_bad_input(order):
    chain = markov.Chain(order)
    try:
        chain.train([])
        assert False
    except ValueError as _: assert True
    try:
        chain.train(None)
        assert False
    except TypeError as _: assert True
    try:
        chain.train(1)
        assert False
    except TypeError as _: assert True

def _test_generate(order):
    chain = markov.Chain(order)
    chain.train([1, 2, 3, 4])
    chain.train([1, 3, 5])
    possible_output = [
        [1, 3, 5],
        [1, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 5],
    ]
    for _ in range(100):
        model = list(chain.finite())
        assert model in possible_output

def _test_generate_from_seed(order):
    chain = markov.Chain(order)
    chain.train([1, 2, 3, 4])
    chain.train([3, 5 ])
    possible_output = [[3, 4], [3, 5]]
    for _ in range(100):
        model = list(chain.finite(3))
        assert model in possible_output
    try:
        model = list(chain.finite(7))
        assert False
    except ValueError as _: assert True

def _test_generate_infinite(order):
    chain = markov.Chain(order)
    a, b  = 1, 2
    chain.train([a, b])
    prev = None
    for i, next_ in enumerate(chain.infinite()):
        if prev == a:
            assert next_ == b
        prev = next_
        if i > 100: break
    assert i > 100

def _test_generate_from_empty_chain(order):
    try:
        markov.Chain(order).finite()
        assert False
    except Exception as _: assert True

# The following test fails:
# 
#       corpus = [True, 1, '1', (0b101, 3.141592653589793)]
#       chain = markov.Chain(order)
#       chain.train(corpus)
#       result = [*chain.finite()]
#       assert result == corpus
# 
# as the interal representation of the chain (order 1)
# produces dictionary keys:
#
#       (True,)
#       (1, )
#
# Even if the caller intended for these values to model
# conceptually distinct phenomenon, Python considers them equal,
# hence, the chain will aggregate their outcomes under
# the first such state train()ed by the model.
#
# Being at the mercy of quirky edge cases caused by duck typing is beyond 
# the scope of this minimalist implementation, thus the Chain API specifies 
# undefined behavior for mixed-type elements.
