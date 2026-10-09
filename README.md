# Ansible Role: Gasket

Builds and installs the Google Gasket DKMS driver for a PCIe Coral TPU on
Ubuntu 24.04. Requires ansible-core 2.16 or newer and sudo access for package
installation.

The role checks both the installed package status and its Debian version. An
installed version equal to or newer than `gasket_dkms_version` is left alone,
without refreshing APT or installing build tools. Missing, removed, or older
packages are rebuilt from the pinned source revision. Builds run as the SSH
user in an isolated temporary directory, which is removed even after failure.
The role installs build dependencies and headers for the running kernel before
installing the built package with privilege escalation.

## Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `gasket_dkms_version` | `1.0-18` | Minimum acceptable Debian package version. |
| `gasket_driver_repository` | `https://github.com/google/gasket-driver.git` | Driver source repository. |
| `gasket_driver_revision` | `5815ee3908a46a415aac616ac7b9aedcb98a504c` | Immutable driver source revision. |

When changing the minimum version, also select a source revision whose Debian
changelog meets that version. The role checks this before building. The role
release version is independent of the driver's Debian package version.

## Example playbook

```yaml
- name: Install Gasket
  hosts: all
  roles:
    - PaulGallon.gasket
```

The role handles its own privilege escalation; play-level `become` and a repeated
`gasket_dkms_version` override are unnecessary. The Edge TPU userspace runtime
and Coral APT repository remain the caller's responsibility.

Check mode reads the installed package and reports whether installation is
needed, without installing packages, cloning source, or building the driver.

## Validation

With `ansible-playbook` on PATH, run `python3 tests/test_package_states.py`.
These tests execute the role with controlled package-query results, covering
Debian version ordering, removed packages, command argument expansion, query
errors, and check mode. Fresh-install build validation should use a disposable
Ubuntu 24.04 host with headers available for its running kernel:

```console
ansible-playbook -i test-host, tests/build.yml
```

`tests/build.yml` verifies that DKMS compiled and installed the driver and that
the temporary build directory was removed. Run it again to check idempotency.
