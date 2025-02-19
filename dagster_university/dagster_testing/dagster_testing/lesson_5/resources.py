import dagster as dg


class ExampleResource(dg.ConfigurableResource):
    api_key: str

    def number_5(self):
        return 5
