from vibe.core.config._migration import migrate_config


def test_active_model_rename_does_not_dangle_with_custom_model_name():
    """Regression for #860.

    When a devstral-2 model entry has a non-standard 'name' (not
    'mistral-vibe-cli-latest'), the old code renamed active_model to
    'mistral-medium-3.5' but left the model alias as 'devstral-2'.
    That mismatch caused:
        Active model 'mistral-medium-3.5' not found in configuration.
    The fix makes the alias rename unconditional.
    """
    data = {
        "active_model": "devstral-2",
        "models": [
            {"alias": "devstral-2", "name": "custom-old-name", "provider": "mistral"}
        ],
    }
    migrate_config(data)
    aliases = {m["alias"] for m in data["models"]}
    assert data["active_model"] in aliases, (
        f"active_model={data['active_model']!r} is dangling, aliases={aliases}"
    )
