"""Undo management for Gaphor.

Undoing and redoing actions is managed through the UndoManager.

An undo action should be a callable object (called with no arguments).

An undo action should return a callable object that acts as redo function.
If None is returned the undo action is considered to be the redo action as well.

NOTE: it would be nice to use actions in conjunction with functools.partial.
"""

import logging
from typing import Callable, List

from gaphas import state

from gaphor.abc import ActionProvider, Service
from gaphor.action import action
from gaphor.core import event_handler
from gaphor.core.modeling.event import (
    AssociationAdded,
    AssociationDeleted,
    AssociationSet,
    AttributeUpdated,
    ElementCreated,
    ElementDeleted,
    ModelReady,
)
from gaphor.core.modeling.properties import association as association_property
from gaphor.event import (
    ActionEnabled,
    ServiceEvent,
    TransactionBegin,
    TransactionCommit,
    TransactionRollback,
)
from gaphor.transaction import Transaction, transactional

logger = logging.getLogger(__name__)


class ActionStack:
    """A transaction.

    Every action that is added between a begin_transaction() and a
    commit_transaction() call is recorded in a transaction, so it can be
    played back when a transaction is executed. This executing a
    transaction has the effect of performing the actions recorded, which
    will typically undo actions performed by the user.
    """

    def __init__(self):
        self._actions: List[Callable[[], None]] = []

    def add(self, action):
        self._actions.append(action)

    def can_execute(self):
        return self._actions and True or False

    @transactional
    def execute(self):
        self._actions.reverse()

        for act in self._actions:
            try:
                act()
            except Exception:
                logger.error(f"Error while undoing action {act}", exc_info=True)


class UndoManagerStateChanged(ServiceEvent):
    """Event class used to send state changes on the Undo Manager."""


class UndoManager(Service, ActionProvider):
    """Simple transaction manager for Gaphor. This transaction manager supports
    nested transactions.

    The Undo manager sports an undo and a redo stack. Each stack
    contains a set of actions that can be executed, just by calling them
    (e.i action()) If something is returned by an action, that is
    considered the callable to be used to undo or redo the last
    performed action.
    """

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self._undo_stack: List[ActionStack] = []
        self._redo_stack: List[ActionStack] = []
        self._stack_depth = 20
        self._current_transaction = None

        event_manager.subscribe(self.reset)
        event_manager.subscribe(self.begin_transaction)
        event_manager.subscribe(self.commit_transaction)
        event_manager.subscribe(self.rollback_transaction)
        self._register_undo_handlers()
        self._action_executed()

    def shutdown(self):
        self.event_manager.unsubscribe(self.reset)
        self.event_manager.unsubscribe(self.begin_transaction)
        self.event_manager.unsubscribe(self.commit_transaction)
        self.event_manager.unsubscribe(self.rollback_transaction)
        self._unregister_undo_handlers()

    def clear_undo_stack(self):
        self._undo_stack = []
        self._current_transaction = None

    def clear_redo_stack(self):
        del self._redo_stack[:]

    @event_handler(ModelReady)
    def reset(self, event=None):
        self.clear_redo_stack()
        self.clear_undo_stack()
        self._action_executed()

    @event_handler(TransactionBegin)
    def begin_transaction(self, event=None):
        """Add an action to the current transaction."""
        assert not self._current_transaction
        self._current_transaction = ActionStack()

    def add_undo_action(self, action):
        """Add an action to undo."""
        if self._current_transaction:
            self._current_transaction.add(action)
            # TODO: should this be placed here?
            self._action_executed()

    @event_handler(TransactionCommit)
    def commit_transaction(self, event=None):
        assert self._current_transaction

        if self._current_transaction.can_execute():
            self.clear_redo_stack()
            self._undo_stack.append(self._current_transaction)
            while len(self._undo_stack) > self._stack_depth:
                del self._undo_stack[0]

        self._current_transaction = None

        self._action_executed()

    @event_handler(TransactionRollback)
    def rollback_transaction(self, event=None):
        """Roll back the transaction we're in."""
        assert self._current_transaction

        # Store stacks
        undo_stack = list(self._undo_stack)

        erroneous_tx = self._current_transaction
        self._current_transaction = None
        try:
            with Transaction(self.event_manager):
                try:
                    erroneous_tx.execute()
                except Exception as e:
                    logger.error("Could not roolback transaction")
                    logger.error(e)
        finally:
            # Discard all data collected in the rollback "transaction"
            self._undo_stack = undo_stack

        self._action_executed()

    def discard_transaction(self):

        self._current_transaction = None

        self._action_executed()

    @action(name="edit-undo", shortcut="<Primary>z")
    def undo_transaction(self):
        if not self._undo_stack:
            return

        if self._current_transaction:
            logger.warning("Trying to undo a transaction, while in a transaction")
            self.commit_transaction()
        transaction = self._undo_stack.pop()

        # Store stacks
        undo_stack = list(self._undo_stack)
        redo_stack = list(self._redo_stack)
        self._undo_stack = []

        try:
            with Transaction(self.event_manager):
                transaction.execute()
        finally:
            # Restore stacks and put latest tx on the redo stack
            self._redo_stack = redo_stack
            if self._undo_stack:
                self._redo_stack.extend(self._undo_stack)
            self._undo_stack = undo_stack

        while len(self._redo_stack) > self._stack_depth:
            del self._redo_stack[0]

        self._action_executed()

    @action(
        name="edit-redo",
        shortcut="<Primary><Shift>z",
    )
    def redo_transaction(self):
        if not self._redo_stack:
            return

        transaction = self._redo_stack.pop()

        redo_stack = list(self._redo_stack)
        try:
            with Transaction(self.event_manager):
                transaction.execute()
        finally:
            self._redo_stack = redo_stack

        self._action_executed()

    def in_transaction(self):
        return self._current_transaction is not None

    def can_undo(self):
        return bool(self._current_transaction or self._undo_stack)

    def can_redo(self):
        return bool(self._redo_stack)

    def _action_executed(self, event=None):
        self.event_manager.handle(ActionEnabled("win.edit-undo", self.can_undo()))
        self.event_manager.handle(ActionEnabled("win.edit-redo", self.can_redo()))
        self.event_manager.handle(UndoManagerStateChanged(self))

    #
    # Undo Handlers
    #

    def _gaphas_undo_handler(self, event):
        self.add_undo_action(lambda: state.saveapply(*event))

    def _register_undo_handlers(self):

        logger.debug("Registering undo handlers")

        self.event_manager.subscribe(self.undo_create_event)
        self.event_manager.subscribe(self.undo_delete_event)
        self.event_manager.subscribe(self.undo_attribute_change_event)
        self.event_manager.subscribe(self.undo_association_set_event)
        self.event_manager.subscribe(self.undo_association_add_event)
        self.event_manager.subscribe(self.undo_association_delete_event)

        #
        # Direct revert-statements from gaphas to the undomanager
        state.observers.add(state.revert_handler)

        state.subscribers.add(self._gaphas_undo_handler)

    def _unregister_undo_handlers(self):

        logger.debug("Unregistering undo handlers")

        self.event_manager.unsubscribe(self.undo_create_event)
        self.event_manager.unsubscribe(self.undo_delete_event)
        self.event_manager.unsubscribe(self.undo_attribute_change_event)
        self.event_manager.unsubscribe(self.undo_association_set_event)
        self.event_manager.unsubscribe(self.undo_association_add_event)
        self.event_manager.unsubscribe(self.undo_association_delete_event)

        state.observers.discard(state.revert_handler)

        state.subscribers.discard(self._gaphas_undo_handler)

    @event_handler(ElementCreated)
    def undo_create_event(self, event):
        factory = event.service
        element = event.element

        def _undo_create_event():
            try:
                del factory._elements[element.id]
            except KeyError:
                pass  # Key was probably already removed in an unlink call
            self.event_manager.handle(ElementDeleted(factory, element))

        self.add_undo_action(_undo_create_event)

    @event_handler(ElementDeleted)
    def undo_delete_event(self, event):
        factory = event.service
        element = event.element

        def _undo_delete_event():
            factory._elements[element.id] = element
            self.event_manager.handle(ElementCreated(factory, element))

        self.add_undo_action(_undo_delete_event)

    @event_handler(AttributeUpdated)
    def undo_attribute_change_event(self, event):
        attribute = event.property
        element = event.element
        value = event.old_value

        def _undo_attribute_change_event():
            attribute._set(element, value)

        self.add_undo_action(_undo_attribute_change_event)

    @event_handler(AssociationSet)
    def undo_association_set_event(self, event):
        association = event.property
        if type(association) is not association_property:
            return
        element = event.element
        value = event.old_value

        def _undo_association_set_event():
            # Tell the association it should not need to let the opposite
            # side connect (it has it's own signal)
            association._set(element, value, from_opposite=True)

        self.add_undo_action(_undo_association_set_event)

    @event_handler(AssociationAdded)
    def undo_association_add_event(self, event):
        association = event.property
        if type(association) is not association_property:
            return
        element = event.element
        value = event.new_value

        def _undo_association_add_event():
            # Tell the association it should not need to let the opposite
            # side connect (it has it's own signal)
            association._del(element, value, from_opposite=True)

        self.add_undo_action(_undo_association_add_event)

    @event_handler(AssociationDeleted)
    def undo_association_delete_event(self, event):
        association = event.property
        if type(association) is not association_property:
            return
        element = event.element
        value = event.old_value

        def _undo_association_delete_event():
            # Tell the assoctaion it should not need to let the opposite
            # side connect (it has it's own signal)
            association._set(element, value, from_opposite=True)

        self.add_undo_action(_undo_association_delete_event)
