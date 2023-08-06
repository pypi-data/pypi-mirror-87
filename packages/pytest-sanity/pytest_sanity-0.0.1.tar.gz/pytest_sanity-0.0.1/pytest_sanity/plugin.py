from _pytest.config import create_terminal_writer


OPT_NAME = '--sanity-group-size'


class ReporterWrapper:
    def __init__(self, config):
        self.terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
        self.terminal_writer = create_terminal_writer(config)

    def msg(self, msg):
        self.terminal_writer.markup(msg, yellow=True)
        self.terminal_reporter.write(msg)


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

    if number_of_test_to_collect is None:
        return

    try:
        del items[number_of_test_to_collect:]
        ReporterWrapper(config).msg('Sanity: Running only first {} tests'.format(number_of_test_to_collect))
    except Exception as e:
        ReporterWrapper(config).msg('Sanity: Something went wrong {}'.format(e))
