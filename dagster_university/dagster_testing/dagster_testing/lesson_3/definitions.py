import dagster as dg

from .assets import CatFacts, cat_facts_with_resource, cat_facts


catfacts_resource = CatFacts()

defs = dg.Definitions(
    assets=[cat_facts, cat_facts_with_resource],
    resources={
        "catfacts_resource": catfacts_resource,
    },
)
