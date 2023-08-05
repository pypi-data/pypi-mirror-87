import pytest

from src.deadlinkz import loadFile, checkUnignoredLinks


def test_valid_file():
    expected = ['https://www.youtube.com/', 'https://gbatemp.net/hi', 'https://gbatemp.net/threads/super-mario-64-is-now-natively-playable-on-android-without-an-emulator.574131/', 'https://twitter.com/home', 'https://sdhoihsdiudshfu.com', 'https://www.youtube.com/watch?v=oHg5SJYRHA0', 'https://github.com/', 'https://9r898ryriewurhuweh.com', 'http://blog.marcussaad.com/?feed=rss2&lang=en', 'https://www.google.com/index.html', 'https://www.google.com/', 'https://www.google.ca']
    loaded = loadFile("index.txt")
    assert loaded == expected


def test_invalid_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        loadFile("this should not work")
    assert pytest_wrapped_e.value.code == 2


def test_valid_ignored_file():
    links = ['https://www.youtube.com/', 'https://gbatemp.net/hi', 'https://gbatemp.net/threads/super-mario-64-is-now-natively-playable-on-android-without-an-emulator.574131/', 'https://twitter.com/home', 'https://sdhoihsdiudshfu.com', 'https://www.youtube.com/watch?v=oHg5SJYRHA0', 'https://github.com/', 'https://9r898ryriewurhuweh.com', 'http://blog.marcussaad.com/?feed=rss2&lang=en', 'https://www.google.com/index.html', 'https://www.google.com/', 'https://www.google.ca']
    expected = ['https://gbatemp.net/hi', 'https://gbatemp.net/threads/super-mario-64-is-now-natively-playable-on-android-without-an-emulator.574131/', 'https://twitter.com/home', 'https://sdhoihsdiudshfu.com', 'https://www.youtube.com/watch?v=oHg5SJYRHA0', 'https://9r898ryriewurhuweh.com', 'http://blog.marcussaad.com/?feed=rss2&lang=en', 'https://www.google.com/index.html', 'https://www.google.ca']
    loaded = checkUnignoredLinks(links, "ignore-urls.txt")
    assert loaded == expected


def test_invalid_ignored_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        checkUnignoredLinks("index.txt", "this should not work")
    assert pytest_wrapped_e.value.code == 2

