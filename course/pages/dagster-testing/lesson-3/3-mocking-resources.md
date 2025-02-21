
---
title: 'Lesson 3: Mocking resources'
module: 'dagster_testing'
lesson: '3'
---

When mocking resources, it can sometimes be easier to mock the methods of the resource itself, rather than those used within the resource.

The `get_authors` method within the `AuthorResource` resource returns slightly different data from Open Library. We can define the mock for this function:

```python
fake_author = {
   "author": "Mark Twain",
   "top_work": "Adventures of Huckleberry Finn",
}

mocked_resource = Mock()
mocked_resource.get_authors.return_value = [fake_author]
```

You can see that we are no longer setting up the mock around `get` and instead are mocking and setting the return value for `get_authors`.

Now when we run the `author_works_with_resource` we can supply our mocked version of the resource rather than an actual initialized AuthorResource resource. Click **View answer** to view it.

```python {% obfuscated="true" %}
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
```

There is no longer a need to patch `requests.get` because the mocked version of the resource does not make a call out to Open Library.

## When to mock a resource

You might be wondering when you should mock a resource as opposed to mocking the methods used. Generally speaking you should mock the methods used by the resource if you are more concerned about testing the functionality of the resource and can mock the methods of the resource if you are more concerned with testing the functionality of the assets.

Mocking a resource itself can help give you more control over the specific output expected for certain functions. This can help make it easier when writing tests for assets that use multiple resources.

