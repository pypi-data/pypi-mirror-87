from __future__ import unicode_literals

from django.test import TestCase
import htmls
from cradmin_legacy.python2_compatibility import mock
from model_mommy import mommy
from future import standard_library

from cradmin_legacy.tests.viewhelpers.cradmin_viewhelpers_testapp.models import FilterTestModel
from cradmin_legacy.viewhelpers.listfilter.base.abstractfilter import AbstractFilter
from cradmin_legacy.viewhelpers.listfilter.base.abstractfilterlist import AbstractFilterList
from cradmin_legacy.viewhelpers.listfilter.base.abstractfilterlistchild import AbstractFilterListChild
from cradmin_legacy.viewhelpers.listfilter.base.exceptions import InvalidFiltersStringError

standard_library.install_aliases()


class MinimalFilterGroupChild(AbstractFilterListChild):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'


class MinimalIntFilter(AbstractFilter):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'

    def get_slug(self):
        return 'i'

    def clean_value(self, value):
        return int(value)


class MinimalStringFilter(AbstractFilter):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'

    def get_slug(self):
        return 's'


class TestAbstractFilterList(TestCase):
    def test_append(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        testchild = MinimalFilterGroupChild()
        filterlist.append(testchild)
        self.assertEqual([testchild], filterlist.children)
        self.assertEqual(filterlist, testchild.filterlist)

    def test_render(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        filterlist.append(MinimalFilterGroupChild())
        filterlist.append(MinimalFilterGroupChild())
        selector = htmls.S(filterlist.render(request=mock.MagicMock()))
        self.assertEqual(2, selector.count('li'))

    def test_set_filters_string_invalid_slug(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        stringfilter = MinimalStringFilter()
        filterlist.append(stringfilter)
        with self.assertRaisesMessage(InvalidFiltersStringError,
                                      '"x" is not a valid filter slug.'):
            filterlist.set_filters_string('x-10')

    def test_set_filters_string(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        intfilter = MinimalIntFilter()
        stringfilter = MinimalStringFilter()
        filterlist.append(intfilter)
        filterlist.append(stringfilter)
        filterlist.set_filters_string('i-10/s-test')
        self.assertEqual(['10'], intfilter.values)
        self.assertEqual(['test'], stringfilter.values)

    def test_filter(self):
        class FilterOne(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mycharfield='test')

        class FilterTwo(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mybooleanfield=True)

        match = mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                           mycharfield='test', mybooleanfield=True)
        mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                   mycharfield='no match', mybooleanfield=True)
        mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                   mycharfield='test', mybooleanfield=False)

        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        filterlist.append(FilterOne(slug='filterone'))
        filterlist.append(FilterTwo(slug='filtertwo'))
        queryset = filterlist.filter(FilterTestModel.objects.all())
        self.assertEqual({match},
                         set(queryset))

    def test_filter_exclude(self):
        class FilterOne(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mycharfield='test')

        class FilterTwo(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mybooleanfield=True)

        match1 = mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                            mycharfield='test', mybooleanfield=True)
        match2 = mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                            mycharfield='no match', mybooleanfield=True)
        mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                   mycharfield='test', mybooleanfield=False)

        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock(), target_dom_id='testdomid')
        filterlist.append(FilterOne(slug='filterone'))
        filterlist.append(FilterTwo(slug='filtertwo'))
        queryset = filterlist.filter(FilterTestModel.objects.all(), exclude={'filterone'})
        self.assertEqual({match1, match2},
                         set(queryset))
