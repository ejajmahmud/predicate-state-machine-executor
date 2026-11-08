"""CLI for predicate-state-machine-executor."""
import sys
import argparse
from .fsm import PredicateStateMachineExecutor


def main():
    parser = argparse.ArgumentParser(description="Predicate State Machine Executor CLI")
    parser.add_argument("--demo", action="store_true", help="Run state machine execution demo")
    args = parser.parse_args()

    if args.demo:
        fsm = PredicateStateMachineExecutor("PLANNING", ["DEPLOYED"])
        fsm.add_transition("PLANNING", "CODING", lambda ctx: ctx.get("spec_approved") is True)
        fsm.add_transition("CODING", "TESTING", lambda ctx: ctx.get("code_written") is True)
        fsm.add_transition("TESTING", "DEPLOYED", lambda ctx: ctx.get("tests_passed") is True)

        ctx = {"spec_approved": True, "code_written": True, "tests_passed": True}
        print(f"[*] Initial State: {fsm.current_state}")
        while not fsm.is_finished():
            s = fsm.step(ctx)
            print(f"  -> Transitioned to: {s}")
        print(f"[+] Final History: {' -> '.join(fsm.history)}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
