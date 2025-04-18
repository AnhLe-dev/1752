from library_item import LibraryItem


def test_library_item_initial_values(capsys):
    item = LibraryItem("Song A", "Artist A", 3)

    assert item.name == "Song A"
    assert item.artist == "Artist A"
    assert item.rating == 3
    assert item.play_count == 0

    with capsys.disabled():
        print(f" tested {item.__class__.__name__} initial values successfully")


def test_library_item_stars(capsys):
    item = LibraryItem("Song B", "Artist B", 4)
    assert item.stars() == "****"

    item.rating = 1
    assert item.stars() == "*"

    item.rating = 0
    assert item.stars() == ""

    with capsys.disabled():
        print(f" tested {item.__class__.__name__} stars() successfully")


def test_library_item_info(capsys):
    item = LibraryItem("Song C", "Artist C", 2)
    expected_info = "Song C - Artist C **"
    assert item.info() == expected_info

    with capsys.disabled():
        print(f" tested {item.__class__.__name__} info() successfully")
