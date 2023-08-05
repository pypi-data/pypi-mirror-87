import unittest

from pyramid.util import text_


class TestPredicateList(unittest.TestCase):
    def _makeOne(self):
        from pyramid import predicates
        from pyramid.config.predicates import PredicateList

        inst = PredicateList()
        for name, factory in (
            ('xhr', predicates.XHRPredicate),
            ('request_method', predicates.RequestMethodPredicate),
            ('path_info', predicates.PathInfoPredicate),
            ('request_param', predicates.RequestParamPredicate),
            ('header', predicates.HeaderPredicate),
            ('accept', predicates.AcceptPredicate),
            ('containment', predicates.ContainmentPredicate),
            ('request_type', predicates.RequestTypePredicate),
            ('match_param', predicates.MatchParamPredicate),
            ('is_authenticated', predicates.IsAuthenticatedPredicate),
            ('custom', predicates.CustomPredicate),
            ('traverse', predicates.TraversePredicate),
        ):
            inst.add(name, factory)
        return inst

    def _callFUT(self, **kw):
        inst = self._makeOne()
        config = DummyConfigurator()
        return inst.make(config, **kw)

    def test_ordering_xhr_and_request_method_trump_only_containment(self):
        order1, _, _ = self._callFUT(xhr=True, request_method='GET')
        order2, _, _ = self._callFUT(containment=True)
        self.assertTrue(order1 < order2)

    def test_ordering_number_of_predicates(self):
        from pyramid.config.predicates import predvalseq

        order0, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            is_authenticated=True,
            containment='containment',
            request_type='request_type',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        order1, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        order2, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        order3, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
        )
        order4, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
            containment='containment',
        )
        order5, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
            accept='accept',
        )
        order6, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
            header='header',
        )
        order7, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            match_param='foo=bar',
        )
        order8, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
        )
        order9, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method', path_info='path_info'
        )
        order10, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method'
        )
        order11, _, _ = self._callFUT(xhr='xhr')
        order12, _, _ = self._callFUT()
        self.assertTrue(order1 > order0)
        self.assertEqual(order1, order2)
        self.assertTrue(order3 > order2)
        self.assertTrue(order4 > order3)
        self.assertTrue(order5 > order4)
        self.assertTrue(order6 > order5)
        self.assertTrue(order7 > order6)
        self.assertTrue(order8 > order7)
        self.assertTrue(order9 > order8)
        self.assertTrue(order10 > order9)
        self.assertTrue(order11 > order10)
        self.assertTrue(order12 > order11)

    def test_ordering_importance_of_predicates(self):
        from pyramid.config.predicates import predvalseq

        order1, _, _ = self._callFUT(xhr='xhr')
        order2, _, _ = self._callFUT(request_method='request_method')
        order3, _, _ = self._callFUT(path_info='path_info')
        order4, _, _ = self._callFUT(request_param='param')
        order5, _, _ = self._callFUT(header='header')
        order6, _, _ = self._callFUT(accept='accept')
        order7, _, _ = self._callFUT(containment='containment')
        order8, _, _ = self._callFUT(request_type='request_type')
        order9, _, _ = self._callFUT(match_param='foo=bar')
        order10, _, _ = self._callFUT(is_authenticated=True)
        order11, _, _ = self._callFUT(
            custom=predvalseq([DummyCustomPredicate()])
        )
        self.assertTrue(order1 > order2)
        self.assertTrue(order2 > order3)
        self.assertTrue(order3 > order4)
        self.assertTrue(order4 > order5)
        self.assertTrue(order5 > order6)
        self.assertTrue(order6 > order7)
        self.assertTrue(order7 > order8)
        self.assertTrue(order8 > order9)
        self.assertTrue(order9 > order10)
        self.assertTrue(order10 > order11)

    def test_ordering_importance_and_number(self):
        from pyramid.config.predicates import predvalseq

        order1, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method'
        )
        order2, _, _ = self._callFUT(
            custom=predvalseq([DummyCustomPredicate()])
        )
        self.assertTrue(order1 < order2)

        order1, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method'
        )
        order2, _, _ = self._callFUT(
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        self.assertTrue(order1 > order2)

        order1, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method', path_info='path_info'
        )
        order2, _, _ = self._callFUT(
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        self.assertTrue(order1 < order2)

        order1, _, _ = self._callFUT(
            xhr='xhr', request_method='request_method', path_info='path_info'
        )
        order2, _, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            custom=predvalseq([DummyCustomPredicate()]),
        )
        self.assertTrue(order1 > order2)

    def test_different_custom_predicates_with_same_hash(self):
        from pyramid.config.predicates import predvalseq

        class PredicateWithHash:
            def __hash__(self):
                return 1

        a = PredicateWithHash()
        b = PredicateWithHash()
        _, _, a_phash = self._callFUT(custom=predvalseq([a]))
        _, _, b_phash = self._callFUT(custom=predvalseq([b]))
        self.assertEqual(a_phash, b_phash)

    def test_traverse_has_remainder_already(self):
        order, predicates, phash = self._callFUT(traverse='/1/:a/:b')
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'traverse': 'abc'}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(info, {'traverse': 'abc'})

    def test_traverse_matches(self):
        order, predicates, phash = self._callFUT(traverse='/1/:a/:b')
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'match': {'a': 'a', 'b': 'b'}}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(
            info, {'match': {'a': 'a', 'b': 'b', 'traverse': ('1', 'a', 'b')}}
        )

    def test_traverse_matches_with_highorder_chars(self):
        order, predicates, phash = self._callFUT(
            traverse=text_(b'/La Pe\xc3\xb1a/{x}', 'utf-8')
        )
        self.assertEqual(len(predicates), 1)
        pred = predicates[0]
        info = {'match': {'x': text_(b'Qu\xc3\xa9bec', 'utf-8')}}
        request = DummyRequest()
        result = pred(info, request)
        self.assertEqual(result, True)
        self.assertEqual(
            info['match']['traverse'],
            (
                text_(b'La Pe\xc3\xb1a', 'utf-8'),
                text_(b'Qu\xc3\xa9bec', 'utf-8'),
            ),
        )

    def test_custom_predicates_can_affect_traversal(self):
        from pyramid.config.predicates import predvalseq

        def custom(info, request):
            m = info['match']
            m['dummy'] = 'foo'
            return True

        _, predicates, _ = self._callFUT(
            custom=predvalseq([custom]), traverse='/1/:dummy/:a'
        )
        self.assertEqual(len(predicates), 2)
        info = {'match': {'a': 'a'}}
        request = DummyRequest()
        self.assertTrue(all([p(info, request) for p in predicates]))
        self.assertEqual(
            info,
            {
                'match': {
                    'a': 'a',
                    'dummy': 'foo',
                    'traverse': ('1', 'foo', 'a'),
                }
            },
        )

    def test_predicate_text_is_correct(self):
        from pyramid.config.predicates import predvalseq

        _, predicates, _ = self._callFUT(
            xhr='xhr',
            request_method='request_method',
            path_info='path_info',
            request_param='param',
            header='header',
            accept='accept',
            containment='containment',
            request_type='request_type',
            custom=predvalseq(
                [
                    DummyCustomPredicate(),
                    DummyCustomPredicate.classmethod_predicate,
                    DummyCustomPredicate.classmethod_predicate_no_text,
                ]
            ),
            match_param='foo=bar',
            is_authenticated=False,
        )
        self.assertEqual(predicates[0].text(), 'xhr = True')
        self.assertEqual(
            predicates[1].text(), "request_method = request_method"
        )
        self.assertEqual(predicates[2].text(), 'path_info = path_info')
        self.assertEqual(predicates[3].text(), 'request_param param')
        self.assertEqual(predicates[4].text(), 'header header')
        self.assertEqual(predicates[5].text(), 'accept = accept')
        self.assertEqual(predicates[6].text(), 'containment = containment')
        self.assertEqual(predicates[7].text(), 'request_type = request_type')
        self.assertEqual(predicates[8].text(), "match_param foo=bar")
        self.assertEqual(predicates[9].text(), "is_authenticated = False")
        self.assertEqual(predicates[10].text(), 'custom predicate')
        self.assertEqual(predicates[11].text(), 'classmethod predicate')
        self.assertTrue(predicates[12].text().startswith('custom predicate'))

    def test_predicate_text_is_correct_when_multiple(self):
        _, predicates, _ = self._callFUT(
            request_method=('one', 'two'),
            request_param=('par2=on', 'par1'),
            header=('header2', 'header1:val.*'),
            accept=('accept1', 'accept2'),
            match_param=('foo=bar', 'baz=bim'),
        )
        self.assertEqual(predicates[0].text(), "request_method = one,two")
        self.assertEqual(predicates[1].text(), 'request_param par1,par2=on')
        self.assertEqual(predicates[2].text(), 'header header1=val.*, header2')
        self.assertEqual(predicates[3].text(), 'accept = accept1, accept2')
        self.assertEqual(predicates[4].text(), "match_param baz=bim,foo=bar")

    def test_match_param_from_string(self):
        _, predicates, _ = self._callFUT(match_param='foo=bar')
        request = DummyRequest()
        request.matchdict = {'foo': 'bar', 'baz': 'bum'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_match_param_from_string_fails(self):
        _, predicates, _ = self._callFUT(match_param='foo=bar')
        request = DummyRequest()
        request.matchdict = {'foo': 'bum', 'baz': 'bum'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_match_param_from_dict(self):
        _, predicates, _ = self._callFUT(match_param=('foo=bar', 'baz=bum'))
        request = DummyRequest()
        request.matchdict = {'foo': 'bar', 'baz': 'bum'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_match_param_from_dict_fails(self):
        _, predicates, _ = self._callFUT(match_param=('foo=bar', 'baz=bum'))
        request = DummyRequest()
        request.matchdict = {'foo': 'bar', 'baz': 'foo'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_request_method_sequence(self):
        _, predicates, _ = self._callFUT(request_method=('GET', 'HEAD'))
        request = DummyRequest()
        request.method = 'HEAD'
        self.assertTrue(predicates[0](Dummy(), request))
        request.method = 'GET'
        self.assertTrue(predicates[0](Dummy(), request))
        request.method = 'POST'
        self.assertFalse(predicates[0](Dummy(), request))

    def test_request_method_ordering_hashes_same(self):
        hash1, _, __ = self._callFUT(request_method=('GET', 'HEAD'))
        hash2, _, __ = self._callFUT(request_method=('HEAD', 'GET'))
        self.assertEqual(hash1, hash2)
        hash1, _, __ = self._callFUT(request_method=('GET',))
        hash2, _, __ = self._callFUT(request_method='GET')
        self.assertEqual(hash1, hash2)

    def test_header_simple(self):
        _, predicates, _ = self._callFUT(header='foo')
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'baz': 'foo'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_header_simple_fails(self):
        _, predicates, _ = self._callFUT(header='content-length')
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'baz': 'foo'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_header_with_value(self):
        _, predicates, _ = self._callFUT(header='foo:bar')
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'baz': 'foo'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_header_with_value_fails(self):
        _, predicates, _ = self._callFUT(header='foo:bar')
        request = DummyRequest()
        request.headers = {'foo': 'nobar', 'baz': 'foo'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_header_with_value_fails_case(self):
        _, predicates, _ = self._callFUT(header='foo:bar')
        request = DummyRequest()
        request.headers = {'foo': 'BAR'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_header_multiple(self):
        _, predicates, _ = self._callFUT(header=('foo', 'content-length'))
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'content-length': '42'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_header_multiple_fails(self):
        _, predicates, _ = self._callFUT(header=('foo', 'content-encoding'))
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'content-length': '42'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_header_multiple_with_values(self):
        _, predicates, _ = self._callFUT(header=('foo:bar', 'spam:egg'))
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'spam': 'eggs'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_header_multiple_with_values_fails(self):
        _, predicates, _ = self._callFUT(header=('foo:bar', 'spam:egg$'))
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'spam': 'eggs'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_header_multiple_mixed(self):
        _, predicates, _ = self._callFUT(header=('foo:bar', 'spam'))
        request = DummyRequest()
        request.headers = {'foo': 'bars', 'spam': 'ham'}
        self.assertTrue(predicates[0](Dummy(), request))

    def test_header_multiple_mixed_fails(self):
        _, predicates, _ = self._callFUT(header=('foo:bar', 'spam'))
        request = DummyRequest()
        request.headers = {'foo': 'nobar', 'spamme': 'ham'}
        self.assertFalse(predicates[0](Dummy(), request))

    def test_is_authenticated_true_matches(self):
        _, predicates, _ = self._callFUT(is_authenticated=True)
        request = DummyRequest()
        request.is_authenticated = True
        self.assertTrue(predicates[0](Dummy(), request))

    def test_is_authenticated_true_fails(self):
        _, predicates, _ = self._callFUT(is_authenticated=True)
        request = DummyRequest()
        request.is_authenticated = False
        self.assertFalse(predicates[0](Dummy(), request))

    def test_is_authenticated_false_matches(self):
        _, predicates, _ = self._callFUT(is_authenticated=False)
        request = DummyRequest()
        request.is_authenticated = False
        self.assertTrue(predicates[0](Dummy(), request))

    def test_is_authenticated_false_fails(self):
        _, predicates, _ = self._callFUT(is_authenticated=False)
        request = DummyRequest()
        request.is_authenticated = True
        self.assertFalse(predicates[0](Dummy(), request))

    def test_unknown_predicate(self):
        from pyramid.exceptions import ConfigurationError

        self.assertRaises(ConfigurationError, self._callFUT, unknown=1)

    def test_predicate_close_matches(self):
        from pyramid.exceptions import ConfigurationError

        with self.assertRaises(ConfigurationError) as context:
            self._callFUT(method='GET')
        expected_msg = (
            "Unknown predicate values: {'method': 'GET'} "
            "(did you mean request_method)"
        )
        self.assertEqual(context.exception.args[0], expected_msg)

    def test_notted(self):
        from pyramid.config import not_
        from pyramid.testing import DummyRequest

        request = DummyRequest()
        _, predicates, _ = self._callFUT(
            xhr='xhr', request_method=not_('POST'), header=not_('header')
        )
        self.assertEqual(predicates[0].text(), 'xhr = True')
        self.assertEqual(predicates[1].text(), "!request_method = POST")
        self.assertEqual(predicates[2].text(), '!header header')
        self.assertEqual(predicates[1](None, request), True)
        self.assertEqual(predicates[2](None, request), True)


class Test_sort_accept_offers(unittest.TestCase):
    def _callFUT(self, offers, order=None):
        from pyramid.config.predicates import sort_accept_offers

        return sort_accept_offers(offers, order)

    def test_default_specificities(self):
        result = self._callFUT(['text/html', 'text/html;charset=utf8'])
        self.assertEqual(result, ['text/html;charset=utf8', 'text/html'])

    def test_specific_type_order(self):
        result = self._callFUT(
            [
                'text/html',
                'application/json',
                'text/html;charset=utf8',
                'text/plain',
            ],
            ['application/json', 'text/html'],
        )
        self.assertEqual(
            result,
            [
                'application/json',
                'text/html;charset=utf8',
                'text/html',
                'text/plain',
            ],
        )

    def test_params_order(self):
        result = self._callFUT(
            [
                'text/html;charset=utf8',
                'text/html;charset=latin1',
                'text/html;foo=bar',
            ],
            ['text/html;charset=latin1', 'text/html;charset=utf8'],
        )
        self.assertEqual(
            result,
            [
                'text/html;charset=latin1',
                'text/html;charset=utf8',
                'text/html;foo=bar',
            ],
        )

    def test_params_inherit_type_prefs(self):
        result = self._callFUT(
            ['text/html;charset=utf8', 'text/plain;charset=latin1'],
            ['text/plain', 'text/html'],
        )
        self.assertEqual(
            result, ['text/plain;charset=latin1', 'text/html;charset=utf8']
        )


class DummyCustomPredicate:
    def __init__(self):
        self.__text__ = 'custom predicate'

    def classmethod_predicate(*args):  # pragma: no cover
        pass

    classmethod_predicate.__text__ = 'classmethod predicate'
    classmethod_predicate = classmethod(classmethod_predicate)

    @classmethod
    def classmethod_predicate_no_text(*args):
        pass  # pragma: no cover


class Dummy:
    def __init__(self, **kw):
        self.__dict__.update(**kw)


class DummyRequest:
    subpath = ()
    matchdict = None

    def __init__(self, environ=None):
        if environ is None:
            environ = {}
        self.environ = environ
        self.params = {}
        self.headers = {}
        self.cookies = {}


class DummyConfigurator:
    package = 'dummy package'
    registry = 'dummy registry'

    def get_settings(self):
        return {}

    def maybe_dotted(self, thing):
        return thing
