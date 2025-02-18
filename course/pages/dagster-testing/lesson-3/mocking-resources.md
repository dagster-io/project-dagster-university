---
title: 'Lesson 3: Resources'
module: 'dagster_testing'
lesson: '3'
---

With our asset rewritten to use a resource. This is one option we can use in terms of mocking. Rather than mocking and patching `requests`, we can mock the resource itself.

If we wanted to mock the resource what would that look like? Click **View answer** to view it.

```python {% obfuscated="true" %}
fake_author = {
    "author": "Mark Twain",
    "top_work": "Adventures of Huckleberry Finn",
}

mocked_resource = Mock()
mocked_resource.get_authors.return_value = [fake_author]
```

The big difference is that we are no longer mocking the `get` method within requests. Instead we are mocking and setting the return value for `get_authors` which is the only method in the resource.

Now we can use the mocked resource within the test itself and execute the asset using the mock. Click **View answer** to view it.

```python {% obfuscated="true" %}
def test_author_mocked_resource():
    fake_author = {
        "author": "Mark Twain",
        "top_work": "Adventures of Huckleberry Finn",
    }

    mocked_resource = Mock()
    mocked_resource.get_authors.return_value = [fake_author]

    result = author_works_with_resource("twain", mocked_resource)

    assert len(result) == 1
    assert result[0] == fake_author
```

## What to mock
Mocking the resource can be 

