import dagster as dg

from .assets import (
    AuthorResource,
    author_works,
    author_works_with_resource,
    author_works_with_resource_config,
)

defs = dg.Definitions(
    assets=[
        author_works,
        author_works_with_resource,
        author_works_with_resource_config,
    ],
    resources={
        "author_resource": AuthorResource(),
    },
)
