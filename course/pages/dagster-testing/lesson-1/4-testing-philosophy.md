---
title: "Lesson 1: Testing philosophy"
module: 'dagster_testing'
lesson: '1'
---

# Testing philosophy

When building a comprehensive test suite for your Dagster project, it's helpful to think about a **defense-in-depth testing strategy** with multiple layers. Each layer serves a specific purpose and trades off speed for confidence.

## The testing pyramid

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Integration & E2E Tests (20%)                 │  ← Real services, Docker, staging
├─────────────────────────────────────────────────────────┤
│  Layer 2: Asset Graph Tests (25%)                       │  ← dg.materialize() with mocks
├─────────────────────────────────────────────────────────┤
│  Layer 1: Direct Function Tests (55%)                   │  ← Call asset functions directly
└─────────────────────────────────────────────────────────┘
```

The philosophy is simple: **test business logic extensively with fast, isolated tests**. Use real implementations sparingly for integration validation.

| Layer | Test Type | Location | Portion |
| ----- | --------- | -------- | ------- |
| 1 | Direct function tests | `tests/unit/test_*.py` | 55% |
| 2 | Asset graph tests | `tests/unit/test_*.py` | 25% |
| 3 | Integration & E2E tests | `tests/integration/test_*.py` | 20% |

## Layer 1: Direct function tests (55%)

**Purpose**: Test asset business logic directly as Python functions.

**When to use**: For EVERY asset. This is the default testing approach.

**Why**: Fast, reliable, easy to debug. No Dagster overhead.

```python
# Asset under test
@dg.asset
def calculate_revenue(orders: list[dict]) -> float:
    return sum(order["price"] * order["quantity"] for order in orders)

# Direct function test - call the asset like a regular function
def test_calculate_revenue():
    mock_orders = [
        {"price": 10.0, "quantity": 2},
        {"price": 25.0, "quantity": 1},
    ]
    
    result = calculate_revenue(mock_orders)
    
    assert result == 45.0
```

**What to test at this layer**:
- Business logic and calculations
- Data transformations
- Edge cases (empty inputs, nulls, invalid data)
- Error conditions

**Characteristics**:
- Runs in milliseconds
- No Dagster context needed
- Provide mock inputs for upstream dependencies
- Test the function, not the framework

## Layer 2: Asset graph tests (25%)

**Purpose**: Test asset materialization, graph execution, and resource integration with mocked resources.

**When to use**: When testing asset interactions, configs, or resource dependencies.

**Why**: Validates Dagster-specific behavior (context, configs, IO managers) without slow external calls.

```python
def test_asset_graph_with_mocked_resource():
    mocked_db = Mock()
    mocked_db.query.return_value = [{"id": 1, "name": "Alice"}]
    
    result = dg.materialize(
        assets=[fetch_users, process_users],
        resources={"database": mocked_db},
    )
    
    assert result.success
    assert result.output_for_node("process_users") == [{"id": 1, "name": "ALICE"}]
```

**What to test at this layer**:
- Asset graph execution order
- Resource injection
- Run configs and asset configs
- Multi-asset interactions
- IO manager behavior
- Partitioned asset logic

**Characteristics**:
- Uses `dg.materialize()` or `build_asset_context()`
- Mock external resources (databases, APIs)
- Validates Dagster integration points
- Slower than Layer 1, but still fast (no I/O)

## Layer 3: Integration & E2E tests (20%)

**Purpose**: Validate real resource connections, external system behavior, and end-to-end workflows.

**When to use**: For critical paths where mock behavior might diverge from reality.

{% callout %}

> 💡 **Smoke Tests**: There's a complementary technique called **smoke testing** that runs all transformations on empty or synthetic data to catch structural errors quickly. Smoke tests are covered in detail in Lesson 5. They fill the gap between fast unit tests and slower integration tests.

> {% /callout %}

**Why**: Catches issues that mocks miss (actual SQL syntax, API quirks, authentication, real system interactions).

```python
@pytest.mark.integration
def test_complete_etl_pipeline(docker_postgres):
    """E2E test: complete pipeline with real database."""
    result = dg.materialize(
        assets=[extract_orders, transform_orders, load_orders],
        resources={"database": docker_postgres},
    )
    
    assert result.success
    
    # Verify data actually landed
    with docker_postgres.get_connection() as conn:
        rows = conn.execute("SELECT COUNT(*) FROM orders").fetchone()
        assert rows[0] > 0
```

**What to test at this layer**:
- Database connection and query execution
- API authentication and response parsing
- Critical business workflows
- Data pipeline end-to-end correctness
- Production configuration validation

**Characteristics**:
- Requires environment setup (credentials, staging systems, Docker)
- Slower (seconds to minutes with real network calls)
- May be skipped in CI without proper environment
- Use pytest markers: `@pytest.mark.integration`
- Use sparingly as final validation

## Test speed guidelines

Each layer has expected speed characteristics. If your tests are slower than expected, it may indicate a problem.

| Layer | Expected Speed | If Slower, Consider |
| ----- | -------------- | ------------------- |
| 1 | < 100ms | Check for hidden I/O |
| 2 | < 500ms | Mock expensive resources |
| 3 | < 60s | Parallelize or reduce scope |

## When NOT to use higher layers

| Don't Use | For | Instead Use |
| --------- | --- | ----------- |
| Layer 2 (materialize) | Testing pure business logic | Layer 1 (direct call) |
| Layer 3 (integration) | Testing error handling | Layer 1/2 with mocked errors |
| Layer 3 (integration) | Rapid iteration during development | Layer 1/2 |
| Layer 3 (integration) | Testing edge cases | Layer 1 with mock inputs |

The default should always be Layer 1 (direct function test). Only move up layers when you need to test Dagster-specific behavior or real integrations.
