"""Core Predicate State Machine Executor implementation."""
from typing import Dict, List, Callable, Optional, Any


class Transition:
    def __init__(self, from_state: str, to_state: str, guard: Callable[[Dict[str, Any]], bool], name: str = ""):
        self.from_state = from_state
        self.to_state = to_state
        self.guard = guard
        self.name = name or f"{from_state}->{to_state}"


class PredicateStateMachineExecutor:
    def __init__(self, initial_state: str, terminal_states: Optional[List[str]] = None):
        self.current_state = initial_state
        self.terminal_states = set(terminal_states or [])
        self.transitions: List[Transition] = []
        self.history: List[str] = [initial_state]

    def add_transition(self, from_state: str, to_state: str, guard: Callable[[Dict[str, Any]], bool], name: str = ""):
        self.transitions.append(Transition(from_state, to_state, guard, name))

    def step(self, context: Dict[str, Any]) -> Optional[str]:
        if self.current_state in self.terminal_states:
            return None  # Finished

        for t in self.transitions:
            if t.from_state == self.current_state:
                if t.guard(context):
                    self.current_state = t.to_state
                    self.history.append(self.current_state)
                    return self.current_state

        raise RuntimeError(f"No valid transition from '{self.current_state}' under current context")

    def is_finished(self) -> bool:
        return self.current_state in self.terminal_states
