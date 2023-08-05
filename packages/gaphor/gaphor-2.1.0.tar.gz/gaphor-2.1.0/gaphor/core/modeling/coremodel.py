# This file is generated by codegen.py. DO NOT EDIT!

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Callable, List, Optional

from gaphor.core.modeling.element import Element
from gaphor.core.modeling.properties import (
    association,
    attribute,
    derived,
    derivedunion,
    enumeration,
    redefine,
    relation_many,
    relation_one,
)

if TYPE_CHECKING:
    from gaphor.UML import Dependency, Namespace, Package
# 8: override Element
# defined above


# 11: override NamedElement
# Define extra attributes defined in UML model
class NamedElement(Element):
    name: attribute[str]
    qualifiedName: derived[List[str]]
    visibility: enumeration
    namespace: relation_one[Namespace]
    clientDependency: relation_many[Dependency]
    supplierDependency: relation_many[Dependency]
    memberNamespace: relation_many[Namespace]


# 41: override PackageableElement
class PackageableElement(NamedElement):
    owningPackage: relation_one[Package]


# 60: override Diagram
# defined in gaphor.core.modeling.diagram


# 51: override Presentation
# defined in gaphor.core.modeling.presentation


class Comment(Element):
    body: attribute[str]
    annotatedElement: relation_many[Element]


# 45: override StyleSheet
# defined in gaphor.core.modeling.presentation


NamedElement.name = attribute("name", str)
Comment.body = attribute("body", str)
# 48: override StyleSheet.styleSheet
# defined in gaphor.core.modeling.presentation

# 57: override Presentation.subject
# defined in gaphor.core.modeling.presentation

# 54: override Element.presentation
# defined in gaphor.core.modeling.presentation

Comment.annotatedElement = association("annotatedElement", Element, opposite="comment")
Element.comment = association("comment", Comment, opposite="annotatedElement")
# 22: override NamedElement.qualifiedName(NamedElement.namespace): derived[List[str]]


def _namedelement_qualifiedname(self) -> List[str]:
    """Returns the qualified name of the element as a tuple."""
    if self.namespace:
        return _namedelement_qualifiedname(self.namespace) + [self.name]
    else:
        return [self.name]


NamedElement.qualifiedName = derived(
    "qualifiedName",
    List[str],
    0,
    1,
    lambda obj: [_namedelement_qualifiedname(obj)],
)
