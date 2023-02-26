import importlib.util
import sys

from trubrics.validations.run import TrubricRun


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
