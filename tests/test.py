#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connect four solver testing program
Usage: python test.py <path to solver binary> <path to file with tests> <--weak if solver is weak>
Test format and tests is taken from here: http://blog.gamesolver.org/solving-connect-four/02-test-protocol/

Copyright (C) 2018 Anton Demchenko <d.flier@yandex.ru>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
import os
import sys


def run(solver, test_file, weak):
    """Runs connect four solver on tests, prints result of each test,
    prints average time spent and accuracy at the end.
    :param: solver is subprocess performing solver's code
    :param: test_file is opened file object containing test
    :param: weak points to weakness of solver
    (see definition of weak solver here http://blog.gamesolver.org/solving-connect-four/01-introduction/)
    """
    tests = test_file.readlines()
    total_time = 0
    total_nodes = 0
    wa_tests = []

    for test_idx, test in enumerate(tests):
        position, answer = test.split()
        answer = int(answer)
        answer = answer // abs(answer) if answer != 0 and weak else answer

        solver.stdin.write(bytes(position + "\n", encoding="ascii"))
        solver.stdin.flush()

        result = solver.stdout.readline().strip().decode(encoding="ascii")
        score, nodes, time = map(int, result.split()[1:])

        about = "OK"
        if score != answer:
            wa_tests.append(test_idx + 1)
            about = "WA expected: {} gotten: {}".format(answer, score)
        print("test:", test_idx + 1, position, "time:", time, about)

        total_time += time
        total_nodes += nodes

    avg_time = total_time / len(tests)
    avg_nodes = total_nodes / len(tests)
    accuracy = (len(tests) - len(wa_tests)) / len(tests)

    print("average time:", avg_time)
    print("accuracy:", accuracy)


if __name__ == "__main__":
    solver_path = sys.argv[1]
    test_path = sys.argv[2]
    weak = False
    if len(sys.argv) >= 4 and sys.argv[3] == "--weak":
        weak = True

    with subprocess.Popen([solver_path, ], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as solver:
        with open(test_path, "r") as test_file:
            run(solver, test_file, weak)
