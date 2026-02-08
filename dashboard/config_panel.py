"""
Configuration Panel - Left side of dashboard
Contains test suite selection, parameters, and run controls
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ConfigPanel:
    def __init__(self, parent, on_run_callback):
        self.parent = parent
        self.on_run_callback = on_run_callback
        
        # Store config values
        self.config = {
            'device_ip': tk.StringVar(value='192.168.1.100'),
            'port': tk.StringVar(value='8080'),
            'timeout': tk.StringVar(value='30'),
            'verbose': tk.BooleanVar(value=False),
            'stop_on_fail': tk.BooleanVar(value=False)
        }
        
        self.build_panel()
    
    def build_panel(self):
        """Build all configuration widgets"""
        
        # Test Suite Selection
        suite_frame = tk.LabelFrame(self.parent, text="1. Test Suite Selection", 
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        suite_frame.pack(fill='x', padx=10, pady=10)
        
        self.suite_combo = ttk.Combobox(suite_frame, state='readonly', width=40)
        self.suite_combo['values'] = (
            'CAN Bus Communication Tests',
            'GPIO Functionality Tests', 
            'Sensor Integration Tests',
            'Power Management Tests'
        )
        self.suite_combo.current(0)
        self.suite_combo.pack(pady=5)
        
        # Info label
        tk.Label(suite_frame, text="12 test cases | Est. duration: 5m 30s", 
                font=('Arial', 8), bg='white', fg='gray').pack()
        
        # Test Parameters
        param_frame = tk.LabelFrame(self.parent, text="2. Test Parameters", 
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        param_frame.pack(fill='x', padx=10, pady=10)
        
        # Device IP
        tk.Label(param_frame, text="Target Device IP:", bg='white').grid(row=0, column=0, sticky='w', pady=5)
        tk.Entry(param_frame, textvariable=self.config['device_ip'], width=30).grid(row=0, column=1, pady=5)
        
        # Port
        tk.Label(param_frame, text="Communication Port:", bg='white').grid(row=1, column=0, sticky='w', pady=5)
        tk.Entry(param_frame, textvariable=self.config['port'], width=30).grid(row=1, column=1, pady=5)
        
        # Timeout
        tk.Label(param_frame, text="Timeout (seconds):", bg='white').grid(row=2, column=0, sticky='w', pady=5)
        tk.Entry(param_frame, textvariable=self.config['timeout'], width=30).grid(row=2, column=1, pady=5)
        
        # Checkboxes
        tk.Checkbutton(param_frame, text="Enable Verbose Logging", 
                      variable=self.config['verbose'], bg='white').grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        tk.Checkbutton(param_frame, text="Stop on First Failure", 
                      variable=self.config['stop_on_fail'], bg='white').grid(row=4, column=0, columnspan=2, sticky='w', pady=5)
        
        # Test Selection (placeholder for alpha)
        test_frame = tk.LabelFrame(self.parent, text="3. Select Individual Tests", 
                                  font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        test_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollable test list
        test_list = tk.Text(test_frame, height=8, width=40, bg='#f9f9f9')
        test_list.pack(fill='both', expand=True)
        test_list.insert('1.0', '☑ test_can_init\n☑ test_can_send\n☑ test_can_receive\n☑ test_gpio_read\n☑ test_gpio_write\n☑ test_sensor_data\n☑ test_i2c_comm')
        test_list.config(state='disabled')  # Read-only for alpha
        
        # Action Buttons
        btn_frame = tk.Frame(self.parent, bg='white')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        # RUN button (functional)
        run_btn = tk.Button(btn_frame, text="▶ RUN TEST SUITE", 
                           command=self.run_tests,
                           bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), 
                           height=2, cursor='hand2')
        run_btn.pack(fill='x', pady=(0, 10))
        
        # Save/Load buttons (non-functional in alpha)
        bottom_btns = tk.Frame(btn_frame, bg='white')
        bottom_btns.pack(fill='x')
        
        tk.Button(bottom_btns, text="Save Config", 
                 command=self.save_current_config).pack(side='left', fill='x', expand=True, padx=(0, 5))
        tk.Button(bottom_btns, text="Load Config",
                 command=self.load_saved_config).pack(side='right', fill='x', expand=True, padx=(5, 0))
    
    def save_current_config(self):
        """Save current configuration to file"""
        from config_manager import ConfigManager
        
        config_data = {
            'suite': self.suite_combo.get(),
            'device_ip': self.config['device_ip'].get(),
            'port': self.config['port'].get(),
            'timeout': self.config['timeout'].get(),
            'verbose': self.config['verbose'].get(),
            'stop_on_fail': self.config['stop_on_fail'].get()
        }
        
        manager = ConfigManager()
        manager.save_config(config_data)
    
    def load_saved_config(self):
        """Load configuration from file"""
        from config_manager import ConfigManager
        
        manager = ConfigManager()
        config_data = manager.load_config()
        
        if config_data:
            # Update UI with loaded values
            if 'suite' in config_data:
                # Find and select the suite in combobox
                suite_value = config_data['suite']
                if suite_value in self.suite_combo['values']:
                    self.suite_combo.set(suite_value)
            
            if 'device_ip' in config_data:
                self.config['device_ip'].set(config_data['device_ip'])
            if 'port' in config_data:
                self.config['port'].set(config_data['port'])
            if 'timeout' in config_data:
                self.config['timeout'].set(config_data['timeout'])
            if 'verbose' in config_data:
                self.config['verbose'].set(config_data['verbose'])
            if 'stop_on_fail' in config_data:
                self.config['stop_on_fail'].set(config_data['stop_on_fail'])

    def run_tests(self):
        """Trigger test execution"""
        config_data = {
            'suite': self.suite_combo.get(),
            'device_ip': self.config['device_ip'].get(),
            'port': self.config['port'].get(),
            'timeout': self.config['timeout'].get(),
            'verbose': self.config['verbose'].get(),
            'stop_on_fail': self.config['stop_on_fail'].get()
        }
        self.on_run_callback(config_data)