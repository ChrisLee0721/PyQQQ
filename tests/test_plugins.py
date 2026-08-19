"""Tests for the plugin system."""

from __future__ import annotations

import pytest

from quonic.plugins import (
    AlgorithmPlugin,
    BackendPlugin,
    PassPlugin,
    Plugin,
    get_plugin,
    list_plugins,
    register_plugin,
)
from quonic.plugins.registry import unregister_plugin

# ---------------------------------------------------------------------------
# 1. Plugin base classes
# ---------------------------------------------------------------------------


def test_plugin_has_name():
    p = Plugin()
    p.name = "test"
    assert p.name == "test"


def test_backend_plugin_abstract():
    bp = BackendPlugin()
    bp.name = "test"
    with pytest.raises(NotImplementedError):
        bp.run(None)


def test_pass_plugin_abstract():
    pp = PassPlugin()
    pp.name = "test"
    with pytest.raises(NotImplementedError):
        pp.run(None)


def test_algorithm_plugin_abstract():
    ap = AlgorithmPlugin()
    ap.name = "test"
    with pytest.raises(NotImplementedError):
        ap.run()


# ---------------------------------------------------------------------------
# 2. Plugin registry
# ---------------------------------------------------------------------------


def test_register_and_get():
    class MyPlugin(Plugin):
        name = "test_register"
        version = "0.1.0"
        description = "test plugin"

    register_plugin(MyPlugin())
    p = get_plugin("test_register")
    assert p is not None
    assert p.name == "test_register"
    unregister_plugin("test_register")


def test_list_plugins():
    class MyPlugin(Plugin):
        name = "test_list"
        version = "0.1.0"

    register_plugin(MyPlugin())
    plugins = list_plugins()
    names = [p["name"] for p in plugins]
    assert "test_list" in names
    unregister_plugin("test_list")


def test_register_duplicate_raises():
    class MyPlugin(Plugin):
        name = "test_dup"

    register_plugin(MyPlugin())
    with pytest.raises(ValueError, match="already registered"):
        register_plugin(MyPlugin())
    unregister_plugin("test_dup")


def test_register_no_name_raises():
    class MyPlugin(Plugin):
        name = ""

    with pytest.raises(ValueError, match="must have a name"):
        register_plugin(MyPlugin())


def test_unregister_nonexistent():
    result = unregister_plugin("nonexistent_plugin_xyz")
    assert result is False
