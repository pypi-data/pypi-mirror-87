def test_import():
    from databroker import catalog

    assert "example" in list(catalog)
    db = catalog["example"]
    run = db[-1]
    assert run.metadata
