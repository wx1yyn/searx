# -*- coding: utf-8 -*-

from searx.testing import SearxTestCase
from searx import plugins
from mock import Mock


def get_search_mock(query, **kwargs):
    return Mock(search_query=Mock(query=query, **kwargs),
                result_container=Mock(answers=set()))


class PluginStoreTest(SearxTestCase):

    def test_PluginStore_init(self):
        store = plugins.PluginStore()
        self.assertTrue(isinstance(store.plugins, list) and len(store.plugins) == 0)

    def test_PluginStore_register(self):
        store = plugins.PluginStore()
        testplugin = plugins.Plugin()
        store.register(testplugin)

        self.assertTrue(len(store.plugins) == 1)

    def test_PluginStore_call(self):
        store = plugins.PluginStore()
        testplugin = plugins.Plugin()
        store.register(testplugin)
        setattr(testplugin, 'asdf', Mock())
        request = Mock(user_plugins=[])
        store.call('asdf', request, Mock())

        self.assertFalse(testplugin.asdf.called)

        request.user_plugins.append(testplugin)
        store.call('asdf', request, Mock())

        self.assertTrue(testplugin.asdf.called)


class SelfIPTest(SearxTestCase):

    def test_PluginStore_init(self):
        store = plugins.PluginStore()
        store.register(plugins.self_info)

        self.assertTrue(len(store.plugins) == 1)

        # IP test
        request = Mock(user_plugins=store.plugins,
                       remote_addr='127.0.0.1')
        request.headers.getlist.return_value = []
        search = get_search_mock(query='ip', pageno=1)
        store.call('post_search', request, search)
        self.assertTrue('127.0.0.1' in search.result_container.answers)

        search = get_search_mock(query='ip', pageno=2)
        store.call('post_search', request, search)
        self.assertFalse('127.0.0.1' in search.result_container.answers)

        # User agent test
        request = Mock(user_plugins=store.plugins,
                       user_agent='Mock')
        request.headers.getlist.return_value = []

        search = get_search_mock(query='user-agent', pageno=1)
        store.call('post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers)

        search = get_search_mock(query='user-agent', pageno=2)
        store.call('post_search', request, search)
        self.assertFalse('Mock' in search.result_container.answers)

        search = get_search_mock(query='user-agent', pageno=1)
        store.call('post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers)

        search = get_search_mock(query='user-agent', pageno=2)
        store.call('post_search', request, search)
        self.assertFalse('Mock' in search.result_container.answers)

        search = get_search_mock(query='What is my User-Agent?', pageno=1)
        store.call('post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers)

        search = get_search_mock(query='What is my User-Agent?', pageno=2)
        store.call('post_search', request, search)
        self.assertFalse('Mock' in search.result_container.answers)
