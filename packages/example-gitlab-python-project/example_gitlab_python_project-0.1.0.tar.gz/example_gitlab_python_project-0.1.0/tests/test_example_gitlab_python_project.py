#!/usr/bin/env python

"""Tests for `example_gitlab_python_project` package."""

import pytest
from example_gitlab_python_project import example_gitlab_python_project


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_hello_world():
    example_gitlab_python_project.hello_world()
