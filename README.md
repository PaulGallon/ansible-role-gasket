# Ansible Role: Gasket

Builds and installs Gasket from the Google repository if `gasket_dkms_version` is newer than the currently installed version.

## Example Playbook

```
- name: Install Gasket
  hosts: all
  roles:
    - gasket
```
