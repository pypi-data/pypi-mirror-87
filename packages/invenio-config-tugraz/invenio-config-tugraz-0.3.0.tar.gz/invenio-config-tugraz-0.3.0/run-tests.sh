#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

python -m check_manifest --ignore ".*-requirements.txt"
python -m sphinx.cmd.build -qnNW docs docs/_build/html
docker-services-cli --verbose up es postgresql redis
python -m pytest
tests_exit_code=$?
docker-services-cli down
exit "$tests_exit_code"
