#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""Cli to query the buildstate from GitLab CI."""

from gitlabcicli import gitlabcicli

if __name__ == "__main__":
    gitlabcicli.main()
