import os
import re

from collections import defaultdict
from junit_xml import TestSuite, TestCase

module_dir = os.path.abspath(os.path.dirname(__file__))

class GUnit:
    def __init__(self, build_dir='.', executable='gdb'):
        self.build_dir = os.path.abspath(os.path.join(build_dir, 'gunit'))

        # Create output directory
        os.makedirs(self.build_dir, exist_ok=True)

        self.logging_file = os.path.join(self.build_dir, 'gdblog')
        self.times_file = os.path.join(self.build_dir, 'gdbtimes')
        self.report_file = os.path.join(self.build_dir, 'report.xml')

        self.log = f'-ex "set logging file {self.logging_file}"'
        self.remote = ''
        self.load = ''

        self.gdb = executable

    # Runs automatic testing on given binary/test suite
    def test(self, path=None):
        # Get scripts
        setup_path = os.path.join(module_dir, 'setup.gdb')
        execute_path = os.path.join(module_dir, 'execute.gdb')

        os.environ["GUNIT_GDBTIMES"] = self.times_file

        # Activate GDB and connect to server
        command = f'{self.gdb} -batch-silent {self.log} -x {setup_path} {self.remote} '

        if path is not None:
            command += f'-ex "file {path}" {self.load} '

        command += f'-x {execute_path}'

        os.system(command)

    def junit(self):
        cases = []

        with open(self.logging_file, "r") as gdblog:
            cases = gdblog.read().split("TESTx")

        test_cases = defaultdict(lambda: [])
        test_no = defaultdict(lambda: 1)

        last_function = None

        deltas = []

        with open(self.times_file, "r") as test_times:
            # Get deltas
            times = test_times.readlines()
            for i in range(int(len(times) / 2)):
                start_time = float(times[2 * i])
                end_time = float(times[2 * i + 1])
                deltas += [end_time - start_time]

        for i, testcase in enumerate(cases[1:]):
            caseparts = testcase.split("BACKTRACE")

            suite = re.search(r"FILE (.*)\n", caseparts[0]).group(1)
            line = re.search(r"LINE (\d+)", caseparts[0]).group(1)
            success = re.search(r"PASS (\d)", caseparts[0]).group(1)
            expected = re.search(r"EXPECT (.+?)\n", caseparts[0]).group(1)
            result = re.search(r"RESULT (.+?)\n", caseparts[0]).group(1)

            function = re.search(r"in (?!gunit_hook|gunit_array)(.*) \(.*?\) at", caseparts[1]).group(1)
            suite = re.search(r"(.*/)*(.*?)\..*", suite).group(2)

            add = True
            tc = None

            if last_function != function:
                tc = TestCase(f"Test{test_no[suite]}", function, deltas[i], "", "", allow_multiple_subelements=True)
                test_no[suite] += 1

            else:
                tc = test_cases[suite][-1]
                tc.elapsed_sec += deltas[i]
                add = False

            last_function = function

            if success != "1":
                fail_message = ""
                if expected != result:
                    fail_message = f"Expected {expected}, received {result}"

                else:
                    fail_message = f"Did not expect {expected}"

                # Failure means assertion fail, error means unexpected fault during the execution of the test
                tc.add_failure_info(fail_message, caseparts[1])

            if add:
                test_cases[suite] += [tc]

        test_suites = []
        for key in test_cases.keys():
            test_suites += [TestSuite(key, test_cases[key])]

        with open(self.report_file, "w") as outxml:
                outxml.write(TestSuite.to_xml_string(test_suites))

    #### STATIC FUNCTIONS ####

    # Generate GUnit.h
    def get_header(build_dir='.'):
        source_path = os.path.join(module_dir, 'GUnit.h')
        destination_path = os.path.abspath(os.path.join(build_dir, 'GUnit.h'))

        with open(source_path, "r") as src, open(destination_path, "w") as dst:
            dst.write(src.read())

    # Configure GUnit for OpenOCD server
    def openOCD(gdb_uri, build_dir='.', executable='gdb'):
        target = GUnit(build_dir, executable)

        target.remote = f'-ex "target remote {gdb_uri}"'
        target.load = '-ex load -ex "monitor reset init"'

        return target

    # Configure GUnit for regular GDB server
    def gdbserver(gdb_uri, build_dir='.'):
        target = GUnit(build_dir)

        target.remote = f'-ex "target remote {gdb_uri}"'

        return target
