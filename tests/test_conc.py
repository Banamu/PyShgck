from pyshgck.conc import simple_thread


class TestConcurrencyUtils(object):

    def test_simple_thread(self):
        thread = simple_thread(lambda: None)
        assert thread.daemon

        thread = simple_thread(lambda: None, daemon=False)
        assert not thread.daemon
