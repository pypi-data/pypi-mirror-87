import pytest
from gi.repository import Gtk

from gaphor import UML
from gaphor.ui.diagrampage import DiagramPage
from gaphor.UML.modelinglanguage import UMLModelingLanguage
from gaphor.UML.toolbox import uml_toolbox_actions


@pytest.fixture
def properties():
    return {}


@pytest.fixture
def tab(event_manager, element_factory, properties):
    diagram = element_factory.create(UML.Diagram)
    tab = DiagramPage(
        diagram, event_manager, element_factory, properties, UMLModelingLanguage()
    )

    window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    window.add(tab.construct())
    window.show()
    yield tab
    window.destroy()


def test_pointer(tab):
    tool = tab.get_tool("toolbox-pointer")

    assert tool


@pytest.mark.parametrize(
    "tool_name",
    [
        "toolbox-comment",
        "toolbox-comment-line",
        # Classes:
        "toolbox-class",
        "toolbox-interface",
        "toolbox-package",
        "toolbox-association",
        "toolbox-dependency",
        "toolbox-generalization",
        "toolbox-implementation",
        # Components:
        "toolbox-component",
        "toolbox-node",
        "toolbox-artifact",
        # Actions:
        "toolbox-action",
        "toolbox-initial-node",
        "toolbox-activity-final-node",
        "toolbox-flow-final-node",
        "toolbox-decision-node",
        "toolbox-fork-node",
        "toolbox-flow",
        # Use cases:
        "toolbox-use-case",
        "toolbox-actor",
        "toolbox-use-case-association",
        "toolbox-include",
        "toolbox-extend",
        # Profiles:
        "toolbox-profile",
        "toolbox-metaclass",
        "toolbox-stereotype",
        "toolbox-extension",
    ],
)
def test_placement_action(tab, tool_name):
    tool = tab.get_tool(tool_name)

    # Ensure the factory is working
    tool.create_item((0, 0))
    tab.diagram.canvas.update()


def test_placement_object_node(tab, element_factory):
    test_placement_action(tab, "toolbox-object-node")
    assert len(element_factory.lselect(UML.ObjectNode)) == 1


def test_placement_partition(tab, element_factory):
    test_placement_action(tab, "toolbox-partition")

    assert len(element_factory.lselect(UML.ActivityPartition)) == 2


def test_uml_toolbox_actions_shortcut_unique():

    shortcuts = {}

    for category, items in uml_toolbox_actions:
        for action_name, label, icon_name, shortcut, *rest in items:
            try:
                shortcuts[shortcut].append(action_name)
            except KeyError:
                shortcuts[shortcut] = [action_name]

    for key, val in list(shortcuts.items()):
        if key is not None:
            assert len(val) == 1, f"Duplicate toolbox shortcut {key} for {val}"
