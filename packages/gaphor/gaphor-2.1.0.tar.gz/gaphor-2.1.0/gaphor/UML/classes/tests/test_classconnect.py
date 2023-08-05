"""Classes related adapter connection tests."""

from gaphor import UML
from gaphor.diagram.tests.fixtures import allow, connect, disconnect, get_connected
from gaphor.UML.classes.dependency import DependencyItem
from gaphor.UML.classes.generalization import GeneralizationItem
from gaphor.UML.classes.interface import InterfaceItem
from gaphor.UML.classes.klass import ClassItem
from gaphor.UML.usecases.actor import ActorItem


def test_dependency_glue(create):
    """Test dependency glue to two actor items."""
    actor1 = create(ActorItem, UML.Actor)
    actor2 = create(ActorItem, UML.Actor)
    dep = create(DependencyItem)

    glued = allow(dep, dep.head, actor1)
    assert glued

    connect(dep, dep.head, actor1)

    glued = allow(dep, dep.tail, actor2)
    assert glued


def test_dependency_connect(create, element_factory):
    """Test dependency connecting to two actor items."""
    actor1 = create(ActorItem, UML.Actor)
    actor2 = create(ActorItem, UML.Actor)
    dep = create(DependencyItem)

    connect(dep, dep.head, actor1)
    connect(dep, dep.tail, actor2)

    assert dep.subject is not None
    assert isinstance(dep.subject, UML.Dependency)
    assert dep.subject in element_factory.select()

    hct = get_connected(dep, dep.head)
    tct = get_connected(dep, dep.tail)
    assert hct is actor1
    assert tct is actor2

    assert actor1.subject is dep.subject.supplier
    assert actor2.subject is dep.subject.client


def test_dependency_reconnection(create):
    """Test dependency reconnection."""
    a1 = create(ActorItem, UML.Actor)
    a2 = create(ActorItem, UML.Actor)
    a3 = create(ActorItem, UML.Actor)
    dep = create(DependencyItem)

    # connect: a1 -> a2
    connect(dep, dep.head, a1)
    connect(dep, dep.tail, a2)

    d = dep.subject

    # reconnect: a1 -> a3
    connect(dep, dep.tail, a3)

    assert d is dep.subject
    assert a1.subject is dep.subject.supplier
    assert a3.subject is dep.subject.client
    assert a2.subject is not dep.subject.client, dep.subject.client


def test_dependency_disconnect(create, element_factory):
    actor1 = create(ActorItem, UML.Actor)
    actor2 = create(ActorItem, UML.Actor)
    dep = create(DependencyItem)

    connect(dep, dep.head, actor1)
    connect(dep, dep.tail, actor2)

    dep_subj = dep.subject
    disconnect(dep, dep.tail)

    assert dep.subject is None
    assert get_connected(dep, dep.tail) is None
    assert dep_subj not in element_factory.select()
    assert dep_subj not in actor1.subject.supplierDependency
    assert dep_subj not in actor2.subject.clientDependency


def test_dependency_reconnect(create):
    """Test dependency reconnection using two actor items."""
    actor1 = create(ActorItem, UML.Actor)
    actor2 = create(ActorItem, UML.Actor)
    dep = create(DependencyItem)

    connect(dep, dep.head, actor1)
    connect(dep, dep.tail, actor2)

    dep_subj = dep.subject
    disconnect(dep, dep.tail)

    # reconnect
    connect(dep, dep.tail, actor2)

    assert dep.subject is not None
    assert dep.subject is not dep_subj  # the old subject has been deleted
    assert dep.subject in actor1.subject.supplierDependency
    assert dep.subject in actor2.subject.clientDependency
    # TODO: test with interface (usage) and component (realization)
    # TODO: test with multiple diagrams (should reuse existing relationships first)


def test_multiple_dependencies(create, element_factory):
    """Test multiple dependencies.

    Dependency should appear in a new diagram, bound on a new dependency
    item.
    """
    actoritem1 = create(ActorItem, UML.Actor)
    actoritem2 = create(ActorItem, UML.Actor)
    actor1 = actoritem1.subject
    actor2 = actoritem2.subject
    dep = create(DependencyItem)

    connect(dep, dep.head, actoritem1)
    connect(dep, dep.tail, actoritem2)

    assert dep.subject
    assert 1 == len(actor1.supplierDependency)
    assert actor1.supplierDependency[0] is dep.subject
    assert 1 == len(actor2.clientDependency)
    assert actor2.clientDependency[0] is dep.subject

    # Do the same thing, but now on a new diagram:

    diagram2 = element_factory.create(UML.Diagram)
    actoritem3 = diagram2.create(ActorItem, subject=actor1)
    actoritem4 = diagram2.create(ActorItem, subject=actor2)
    dep2 = diagram2.create(DependencyItem)

    connect(dep2, dep2.head, actoritem3)
    cinfo = diagram2.canvas.get_connection(dep2.head)
    assert cinfo is not None
    assert cinfo.connected is actoritem3
    connect(dep2, dep2.tail, actoritem4)
    assert dep2.subject is not None
    assert 1 == len(actor1.supplierDependency)
    assert actor1.supplierDependency[0] is dep.subject
    assert 1 == len(actor2.clientDependency)
    assert actor2.clientDependency[0] is dep.subject

    assert dep.subject is dep2.subject


def test_dependency_type_auto(create, element_factory):
    """Test dependency type automatic determination."""
    cls = create(ClassItem, UML.Class)
    iface = create(InterfaceItem, UML.Interface)
    dep = create(DependencyItem)

    assert dep.auto_dependency

    connect(dep, dep.tail, cls)  # connect client
    connect(dep, dep.head, iface)  # connect supplier

    assert dep.subject is not None
    assert isinstance(dep.subject, UML.Usage), dep.subject
    assert dep.subject in element_factory.select()


def test_generalization_glue(create):
    """Test generalization item gluing using two classes."""

    gen = create(GeneralizationItem)
    c1 = create(ClassItem, UML.Class)
    c2 = create(ClassItem, UML.Class)

    glued = allow(gen, gen.tail, c1)
    assert glued

    connect(gen, gen.tail, c1)
    assert get_connected(gen, gen.tail) is c1
    assert gen.subject is None

    glued = allow(gen, gen.head, c2)
    assert glued


def test_generalization_connection(create):
    """Test generalization item connection using two classes."""
    gen = create(GeneralizationItem)
    c1 = create(ClassItem, UML.Class)
    c2 = create(ClassItem, UML.Class)

    connect(gen, gen.tail, c1)
    assert get_connected(gen, gen.tail) is c1

    connect(gen, gen.head, c2)
    assert gen.subject is not None
    assert gen.subject.general is c2.subject
    assert gen.subject.specific is c1.subject


def test_generalization_reconnection(create, element_factory):
    """Test generalization item connection using two classes.

    On reconnection a new Generalization is created.
    """
    gen = create(GeneralizationItem)
    c1 = create(ClassItem, UML.Class)
    c2 = create(ClassItem, UML.Class)

    connect(gen, gen.tail, c1)
    assert get_connected(gen, gen.tail) is c1

    connect(gen, gen.head, c2)
    assert gen.subject is not None
    assert gen.subject.general is c2.subject
    assert gen.subject.specific is c1.subject

    # Now do the same on a new diagram:
    diagram2 = element_factory.create(UML.Diagram)
    c3 = diagram2.create(ClassItem, subject=c1.subject)
    c4 = diagram2.create(ClassItem, subject=c2.subject)
    gen2 = diagram2.create(GeneralizationItem)

    connect(gen2, gen2.head, c3)
    cinfo = diagram2.canvas.get_connection(gen2.head)
    assert cinfo is not None
    assert cinfo.connected is c3

    connect(gen2, gen2.tail, c4)
    assert gen.subject is not gen2.subject
    assert len(c1.subject.generalization) == 1
    assert c1.subject.generalization[0] is gen.subject
    # self.assertEqual(1, len(actor2.clientDependency))
    # self.assertTrue(actor2.clientDependency[0] is dep.subject)


def test_generalization_reconnection2(create):
    """Test reconnection of generalization."""
    c1 = create(ClassItem, UML.Class)
    c2 = create(ClassItem, UML.Class)
    c3 = create(ClassItem, UML.Class)
    gen = create(GeneralizationItem)

    # connect: c1 -> c2
    connect(gen, gen.head, c1)
    connect(gen, gen.tail, c2)

    s = gen.subject

    # reconnect: c2 -> c3
    connect(gen, gen.tail, c3)

    assert s is gen.subject
    assert c1.subject is gen.subject.general
    assert c3.subject is gen.subject.specific
    assert c2.subject is not gen.subject.specific
