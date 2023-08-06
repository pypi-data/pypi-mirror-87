# -*- coding: utf-8 -*-
"""Tests for processing.extracting module."""

from os.path import expanduser

from nose.tools import assert_equal
from pybliometrics.scopus import ScopusSearch

from sosia.processing import find_location, parse_docs, get_main_field

refresh = 30
test_cache = expanduser("~/.sosia/") + "test.sqlite"
test_id = 6701809842


def test_find_location():
    pubs = ScopusSearch(f"AU-ID({test_id})", refresh=refresh).results
    ctry, aid, aff = find_location([str(test_id)], pubs, 2000, refresh=30)
    assert_equal(ctry, "Germany")
    assert_equal(aid, "60028717")
    assert_equal(aff, "University of Munich")


def test_get_main_field():
    fields = [1000, 1000, 2000, 2000, 2020, 2020]
    received = get_main_field(fields)
    expected = (2020, "ECON")
    assert_equal(received, expected)


def test_parse_docs():
    eids = ["2-s2.0-84866317084"]
    received = parse_docs(eids, refresh=refresh)
    expected_refs = ('29144517611 57849112238 51249091642 70449099678 '
                     '84865231386 15944370019 8744256776 0004256525 '
                     '84866333650 78650692566 0002969912 0007622058 '
                     '0000169440 0003685848 43049125937 43149086011 '
                     '84866332328 27744606594 2442709303 84866309814 '
                     '34248571923 0029824384 34548317343 3142544611 '
                     '84981198417 0003457562 0032394091 0001116544 '
                     '84866324358 23944478214 0039484749 0001275239 '
                     '34249696486 70449641263 0035654659 0041099301 '
                     '55049124635 67650248718 39149084479 40749109418 '
                     '35348862941 0030559826 34547860480 77953702055 '
                     '18144372897 0004062815 84972591424 0034423919 '
                     '0033675552 0034424078 0027767147 0035654590 '
                     '4243112264 29144486677 0004164119 85015576166 '
                     '33645383647 84981213068 23044470851 78649697033 '
                     '2442654430 0141625872 30444461409 0034435025 '
                     '47949124687 84920182751 84887864855 84866332329 '
                     '84984932935 33845620645 0942299814')
    assert_equal(received[0], expected_refs)
    expected_abs = (
        "Through an analysis of 497 foreign researchers in Italy "
        "and Portugal we verify the impact of home linkages on return "
        "mobility choices and scientific productivity. We consider the "
        "presence of several different types of linkages of the researchers "
        "working abroad with their country of origin and control for the "
        "most relevant contextual factors (age, research area, position in "
        "the host country, etc.). The probability of return to their home "
        "country and scientific productivity in the host country are both "
        "higher for researchers that maintain home linkages. We conclude "
        "that the presence of home linkages directly benefits both "
        "countries in addition to the indirect benefit of expanding the "
        "scientific networks. Policy implications and suggestions for "
        "further research are discussed."
    )
    assert_equal(received[2], expected_abs)
