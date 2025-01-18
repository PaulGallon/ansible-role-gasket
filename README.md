# Ansible Role: Gasket

Builds and installs Gasket from the Google repository if `gasket_dkms_version` is newer than the currently installed version.

## Purpose

I was trying to get my Coral TPU working on Ubuntu 24.04 but I couldn't find a prebuilt version of Gasket new enough so I made this quick role.

## Example Playbook

```
- name: Install Gasket
  hosts: all
  roles:
    - gasket
```
