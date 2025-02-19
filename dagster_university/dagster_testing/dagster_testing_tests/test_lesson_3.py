from unittest.mock import Mock, patch

import dagster as dg

from dagster_testing.lesson_3.assets import (
    API_URL,
    AuthorConfig,
    AuthorResource,
    author_works,
    author_works_with_resource,
    author_works_with_resource_config,
)

EXAMPLE_RESPONSE = {
    "numFound": 2,
    "docs": [
        {
            "name": "Mark Twain",
            "top_work": "Adventures of Huckleberry Finn",
        },
        {
            "name": "Mark Twain Media",
            "top_work": "Easy Science Experiments, Grades 4 - 6+",
        },
    ],
}


@patch("requests.get")
def test_author(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = author_works()

    assert len(result) == 2
    assert result[0] == {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }
    mock_get.assert_called_once_with(API_URL, params={"q": "Twain"})


@patch("requests.get")
def test_author_resource_mock(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = author_works_with_resource(AuthorResource())

    assert len(result) == 2
    assert result[0] == {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }
    mock_get.assert_called_once_with(API_URL, params={"q": "Twain"})


@patch("requests.get")
def test_author_assets_config(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = EXAMPLE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = dg.materialize(
        assets=[author_works_with_resource_config],
        resources={"author_resource": AuthorResource()},
        run_config=dg.RunConfig(
            {"author_works_with_resource_config": AuthorConfig(name="Twain")}
        ),
    )
    assert result.success


def test_author_mocked_resource():
    fake_author = {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }

    mocked_resource = Mock()
    mocked_resource.get_authors.return_value = [fake_author]

    result = author_works_with_resource(mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_author
