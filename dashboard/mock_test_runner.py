"""
Mock Test Runner - Simulates pytest execution for alpha demo
In beta version, this will be replaced with real subprocess calls to pytest
"""

import time
import random
from datetime import datetime


class MockTestRunner:
    def __init__(self, results_panel):
        self.results_panel = results_panel
        self.is_running = False
    
    def run_tests(self, config):
        """Simulate running a test suite"""
        if self.is_running:
            self.results_panel.add_log('[WARNING] Tests already running!')
            return
        
        self.is_running = True
        self.results_panel.clear_results()
        
        # Mock test cases based on selected suite
        test_suite = config['suite']
        mock_tests = self.get_mock_tests(test_suite)
        
        # Start execution
        self.results_panel.update_status("Running...")
        self.results_panel.add_log(f'\n[INFO] Starting test suite: {test_suite}')
        self.results_panel.add_log(f'[INFO] Target device: {config["device_ip"]}:{config["port"]}')
        self.results_panel.add_log(f'[INFO] Timeout: {config["timeout"]}s')
        self.results_panel.add_log('[INFO] Connecting to device...')
        
        # Simulate connection delay
        self.results_panel.parent.after(500, lambda: self._run_test_sequence(mock_tests, config))
    
    def _run_test_sequence(self, tests, config):
        """Run tests one by one with delays"""
        self.results_panel.add_log('[INFO] Connection established!')
        self.results_panel.add_log(f'[INFO] Running {len(tests)} tests...\n')
        
        # Run each test with delay
        self._execute_test(tests, 0, config, datetime.now())
    
    def _execute_test(self, tests, index, config, start_time):
        """Execute a single test (recursive with delays for animation)"""
        if index >= len(tests):
            # All tests complete
            self._finish_execution(tests, start_time)
            return
        
        test = tests[index]
        self.results_panel.add_log(f'[INFO] Running {test["name"]}...')
        
        # Simulate test execution time
        delay = random.randint(300, 800)
        
        def complete_test():
            # Determine pass/fail
            status = 'PASSED' if test['should_pass'] else 'FAILED'
            duration = f"{random.uniform(0.1, 2.5):.2f}s"
            
            # Log result
            if status == 'PASSED':
                self.results_panel.add_log(f'[PASS] {test["name"]} ({duration})')
            else:
                self.results_panel.add_log(f'[FAIL] {test["name"]} ({duration})')
                self.results_panel.add_log(f'[ERROR] {test["error_msg"]}')
            
            # Add to results table
            self.results_panel.add_test_result(test['name'], status, duration)
            
            # Update stats
            passed = sum(1 for t in tests[:index+1] if t['should_pass'])
            failed = (index + 1) - passed
            elapsed = (datetime.now() - start_time).total_seconds()
            duration_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
            self.results_panel.update_stats(index + 1, passed, failed, duration_str)
            
            # Move to next test
            self.results_panel.parent.after(200, lambda: self._execute_test(tests, index + 1, config, start_time))
        
        self.results_panel.parent.after(delay, complete_test)
    
    def _finish_execution(self, tests, start_time):
        """Complete test execution"""
        total = len(tests)
        passed = sum(1 for t in tests if t['should_pass'])
        failed = total - passed
        
        elapsed = (datetime.now() - start_time).total_seconds()
        duration_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
        
        self.results_panel.add_log(f'\n[INFO] Test execution complete!')
        self.results_panel.add_log(f'[INFO] Results: {passed} passed, {failed} failed, {total} total')
        self.results_panel.add_log(f'[INFO] Duration: {duration_str}')
        
        if failed > 0:
            self.results_panel.update_status("Complete - Some tests failed")
        else:
            self.results_panel.update_status("Complete - All tests passed")
        
        self.is_running = False
    
    def get_mock_tests(self, suite_name):
        """Return mock tests based on suite selection"""
        test_suites = {
            'CAN Bus Communication Tests': [
                {'name': 'test_can_init', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_can_send', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_can_receive', 'should_pass': False, 'error_msg': 'Timeout waiting for CAN response'},
                {'name': 'test_can_error_handling', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_can_bus_off', 'should_pass': True, 'error_msg': ''},
            ],
            'GPIO Functionality Tests': [
                {'name': 'test_gpio_read', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_gpio_write', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_gpio_toggle', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_gpio_interrupt', 'should_pass': False, 'error_msg': 'Interrupt not triggered'},
            ],
            'Sensor Integration Tests': [
                {'name': 'test_sensor_init', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_sensor_data_read', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_i2c_communication', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_sensor_calibration', 'should_pass': False, 'error_msg': 'Calibration values out of range'},
            ],
            'Power Management Tests': [
                {'name': 'test_power_on_sequence', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_voltage_monitoring', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_low_power_mode', 'should_pass': True, 'error_msg': ''},
                {'name': 'test_power_failure_recovery', 'should_pass': True, 'error_msg': ''},
            ]
        }
        
        return test_suites.get(suite_name, test_suites['CAN Bus Communication Tests'])