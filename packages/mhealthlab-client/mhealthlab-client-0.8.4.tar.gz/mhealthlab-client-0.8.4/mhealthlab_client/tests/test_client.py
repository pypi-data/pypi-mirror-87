from ..client import Client


def test_extract_participant_list():
    pids = Client.extract_participant_list('sample_participant_list.txt')
    results = [
        "smeltingexerciserstabilize@timestudy_com",
        "shaftbribezippy@timestudy_com",     "marchtumblingoutbid@timestudy_com",
        "lyricallymalformedrigor@timestudy_com",
        "retrypercentdayroom@timestudy_com",
        "showplacefacingsanta@timestudy_com",
        "wrongedsheetentryway@timestudy_com"]
    for pid, result in zip(pids, results):
        assert pid == result
