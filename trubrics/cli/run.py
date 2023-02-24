import importlib.util
import sys

from rich import print as rprint

from trubrics.validations.run import TrubricRun, run_trubric


def import_python_module(module_path: str):
    try:
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        lib = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["module.name"] = lib
        spec.loader.exec_module(lib)  # type: ignore
    except AttributeError:
        raise AttributeError(f"Trubrics config {module_path} is not a python module.")
    return lib


def validate_trubric_run_context(trubric_run_path: str):
    tc = import_python_module(module_path=trubric_run_path)

    if hasattr(tc, "RUN_CONTEXT"):
        if not isinstance(tc.RUN_CONTEXT, TrubricRun):
            raise TypeError("'RUN_CONTEXT' attribute must be of type TrubricRun.")
    else:
        raise AttributeError("Trubrics config python module must contain an attribute 'RUN_CONTEXT'.")
    return tc


def generate_new_trubric(tc):
    all_validation_results = run_trubric(tr=tc.RUN_CONTEXT)
    validations = []
    for validation_result in all_validation_results:
        validations.append(validation_result)

        message_start = f"{validation_result.validation_type} [{validation_result.severity.upper()}]"
        completed_dots = f"[grey82]{(100 - len(message_start)) * '.'}[grey82]"
        message_end = (
            f"[bold {'green' if validation_result.outcome == 'pass' else 'red'}]{validation_result.outcome.upper()}"
        )
        rprint(message_start + completed_dots + message_end)

    new_trubric = tc.trubric
    new_trubric.validations = validations
    return new_trubric
