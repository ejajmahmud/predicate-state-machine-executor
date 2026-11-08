"""Unit tests for predicate-state-machine-executor."""
import unittest
from predicate_state_machine_executor.fsm import PredicateStateMachineExecutor


class TestPredicateStateMachineExecutor(unittest.TestCase):
    def test_transition_success(self):
        fsm = PredicateStateMachineExecutor("INIT", ["DONE"])
        fsm.add_transition("INIT", "DONE", lambda ctx: ctx.get("ready") is True)
        fsm.step({"ready": True})
        self.assertEqual(fsm.current_state, "DONE")
        self.assertTrue(fsm.is_finished())

    def test_blocked_transition_raises(self):
        fsm = PredicateStateMachineExecutor("INIT")
        fsm.add_transition("INIT", "WORKING", lambda ctx: False)
        with self.assertRaises(RuntimeError):
            fsm.step({})
