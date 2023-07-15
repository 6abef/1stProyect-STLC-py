from STLC_proj import lexer_int, lexer_variable
# content of test_sample.py
def inc(x):
    return x + 2


def test_answer():
    assert inc(6) == 8
    
