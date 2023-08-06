# -*- coding: utf-8 -*-
"""Tests for processing.nlp module."""

import warnings

from nose.tools import assert_equal, assert_true
from numpy import array
from scipy.sparse import csr_matrix

from sosia.processing import clean_abstract, compute_cosine

warnings.filterwarnings("ignore")


def test_clean_abstract():
    expected = "Lorem ipsum."
    assert_equal(clean_abstract("Lorem ipsum. © dolor sit."), expected)
    assert_equal(clean_abstract("© dolor sit. Lorem ipsum."), expected)
    assert_equal(clean_abstract(expected), expected)


def test_compute_cos():
    expected = 0.6875
    received = compute_cosine(csr_matrix(array([[0.5, 0.75], [1, 0.25]])))
    assert_equal(received, expected)
