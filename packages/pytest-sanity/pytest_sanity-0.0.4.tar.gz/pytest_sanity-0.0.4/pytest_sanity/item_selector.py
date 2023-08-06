from _pytest.config import create_terminal_writer


class ReporterWrapper:
    def __init__(self, config):
        self.terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
        self.terminal_writer = create_terminal_writer(config)

    def msg(self, msg):
        self.terminal_writer.markup(msg, yellow=True)
        self.terminal_reporter.write(msg)


class ItemSelector:
    def __init__(self, config, items, number_of_test_to_collect):
        self.config = config
        self.items = items
        self.number_of_test_to_collect = number_of_test_to_collect
        self.reporter = ReporterWrapper(config)

    def _get_item_markers(self, item):
        return [marker.name for marker in item.own_markers]

    def _filter_by_mark(self):
        marker = self.config.getoption('-m')
        if marker:
            self.items = [item for item in self.items if marker in self._get_item_markers(item)]

    def _filter_skips(self):
        self.items = [item for item in self.items if 'skip' not in [mark.name for mark in item.iter_markers()]]

    def get(self):
        self._filter_skips()
        self._filter_by_mark()

        try:
            del self.items[self.number_of_test_to_collect:]
            self.reporter.msg('Sanity: Running only first {} tests'.format(self.number_of_test_to_collect))
            return self.items
        except Exception as e:
            self.reporter.msg('Sanity: Something went wrong {}'.format(e))
