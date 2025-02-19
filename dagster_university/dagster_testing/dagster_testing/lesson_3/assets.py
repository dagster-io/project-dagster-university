import dagster as dg
import requests

API_URL = "https://openlibrary.org/search/authors.json"


@dg.asset
def author_works() -> list:
    output = []
    try:
        response = requests.get(API_URL, params={"q": "Twain"})
        response.raise_for_status()

        for doc in response.json().get("docs"):
            output.append(
                {
                    "author": doc.get("name"),
                    "top_work": doc.get("top_work"),
                }
            )

        return output

    except requests.exceptions.RequestException:
        return output


class AuthorResource(dg.ConfigurableResource):
    def get_authors(self, author: str) -> list:
        output = []
        try:
            response = requests.get(API_URL, params={"q": author})
            response.raise_for_status()

            for doc in response.json().get("docs"):
                output.append(
                    {
                        "author": doc.get("name"),
                        "top_work": doc.get("top_work"),
                    }
                )

            return output

        except requests.exceptions.RequestException:
            return output


@dg.asset
def author_works_with_resource(author_resource: AuthorResource) -> list:
    return author_resource.get_authors("Twain")


class AuthorConfig(dg.Config):
    name: str


@dg.asset
def author_works_with_resource_config(
    config: AuthorConfig, author_resource: AuthorResource
) -> list:
    return author_resource.get_authors(config.name)
