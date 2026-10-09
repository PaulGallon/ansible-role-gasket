"""Run the real role's package decisions without changing the test host."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROLE = Path(__file__).resolve().parents[1]
CASES = [
    ("equal", "installed", "1.0-18", 0, False, False),
    ("newer", "installed", "1.0-19", 0, False, False),
    ("debian_suffix", "installed", "1.0-18ubuntu1", 0, False, False),
    ("epoch", "installed", "1:1.0-1", 0, False, False),
    ("older", "installed", "1.0-17", 0, True, False),
    ("prerelease", "installed", "1.0-18~test1", 0, True, False),
    ("missing", "", "", 1, True, False),
    ("removed", "config-files", "1.0-18", 0, True, False),
    ("unconfigured", "unpacked", "1.0-18", 0, True, False),
    ("query_error", "", "", 2, True, True),
]

with tempfile.TemporaryDirectory(prefix="gasket-tests-") as directory:
    root = Path(directory)
    config = root / "ansible.cfg"
    config.write_text("[defaults]\n")
    binary = root / "dpkg-query"
    binary.write_text(r'''#!/usr/bin/env python3
import os
import sys
assert sys.argv[1:] == ["-W", "-f=${db:Status-Status}\\n${Version}", "gasket-dkms"], sys.argv
if os.environ["TEST_QUERY_RC"] == "0":
    print(os.environ["TEST_STATUS"])
    print(os.environ["TEST_VERSION"])
sys.exit(int(os.environ["TEST_QUERY_RC"]))
''')
    binary.chmod(0o755)
    playbook = root / "test.yml"
    playbook.write_text(json.dumps([{
        "hosts": "localhost",
        "gather_facts": False,
        "roles": [str(ROLE)],
        "tasks": [{
            "name": "Assert package decision",
            "ansible.builtin.assert": {
                "that": ["gasket_dkms_version_acceptable == expected_acceptable"]
            },
        }],
    }]))
    for name, status, version, rc, needs_install, fails in CASES:
        environment = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}",
                           ANSIBLE_CONFIG=str(config), ANSIBLE_LOCAL_TEMP=str(root / "local"),
                           TEST_STATUS=status, TEST_VERSION=version, TEST_QUERY_RC=str(rc),
                           Version="argument-expansion-must-be-disabled")
        command = ["ansible-playbook", "-i", "localhost,", "-c", "local",
                   str(playbook), "-e", json.dumps({"expected_acceptable": not needs_install})]
        # Real runs of equal/newer versions must also avoid all package mutations.
        if needs_install:
            command.append("--check")
        result = subprocess.run(command, env=environment, text=True, capture_output=True)
        output = result.stdout + result.stderr
        assert (result.returncode != 0) == fails, (name, output)
        if not fails:
            assert f"changed={int(needs_install)}" in output, (name, output)
        else:
            assert "Check the installed Gasket package status" in output, output
        print(f"PASS {name}")
