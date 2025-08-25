from cf_td import get_greeting

def test_default_greeting():
    assert get_greeting() == "Hello, World!"


def test_custom_greeting():
    assert get_greeting("Alice") == "Hello, Alice!"
