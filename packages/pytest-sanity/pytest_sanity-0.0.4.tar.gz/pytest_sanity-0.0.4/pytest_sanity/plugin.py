from .item_selector import ItemSelector


OPT_NAME = '--sanity-group-size'


def pytest_addoption(parser):
    group = parser.getgroup('sanity')
    group.addoption(
        OPT_NAME,
        type=int,
        help='number of test to run before ending the session successfuly',
        default=None,
    )


def pytest_collection_modifyitems(session, config, items):
    number_of_test_to_collect = config.getoption(OPT_NAME)
    sanity_items = ItemSelector(config, items, number_of_test_to_collect).get()

    del items[:]
    items.extend(sanity_items)
