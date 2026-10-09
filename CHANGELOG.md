# Changelog

## 1.0.0

- Query package status with literal command arguments, without `!unsafe` YAML.
- Accept equal or newer installed packages using Debian version ordering; do
  not mistake removed or unpacked packages for a completed installation.
- Skip APT refreshes and build dependencies when the driver is already current.
- Install compiler tools and headers for the running kernel before DKMS setup.
- Clone and build as the connection user in an isolated temporary directory,
  find the resulting package without a shell pipeline, and clean up on failure.
- Expose pinned source configuration and check its package version before building.
- Support check mode without cloning, building, or changing installed packages.
- Require ansible-core 2.16 or newer and add package-state regression tests.
