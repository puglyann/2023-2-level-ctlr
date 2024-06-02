"""
Public module for checking student CoNLL-U files.
"""

import subprocess
import sys
from pathlib import Path

from config.cli_unifier import _run_console_tool, choose_python_exe
from config.stage_1_style_tests.common import check_result


def check_via_official_validator(conllu_path: Path) -> subprocess.CompletedProcess:
    """
    Run validator checks for the project.

    URL: https://github.com/UniversalDependencies/tools/blob/master/validate.py

    Args:
        paths (list[Path]): Paths to the projects.
        path_to_config (Path): Path to the config.

    Returns:
        subprocess.CompletedProcess: Program execution values
    """
    validator_args = [
        str(Path(__file__).parent / "ud_validator" / "validate.py"),
        "--lang",
        "ru",
        "--max-err",
        "0",
        "--level",
        "2",
        str(conllu_path),
    ]
    return _run_console_tool(str(choose_python_exe()), validator_args, debug=True)


def main() -> None:
    """
    Module entrypoint.
    """
    if len(sys.argv) < 2:
        print('Provide path to the file to check.')
        sys.exit(1)
    conllu_path = Path(sys.argv[1])
    if not conllu_path.exists():
        print("Total CONLLU file is not present. Analyze first.")
        sys.exit(1)

    completed_process = check_via_official_validator(conllu_path=conllu_path)
    print(completed_process.stdout.decode("utf-8"))
    print(completed_process.stderr.decode("utf-8"))
    check_result(completed_process.returncode)


if __name__ == "__main__":
    main()
