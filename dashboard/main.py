"""
HiL Test Automation Dashboard - Main Entry point
Alpha version - GUI Framework with Mock Test Execution
"""
import tkinter as tk
from tkinter import ttk
from config_panel import ConfigPanel # Left Panel - Config
from results_panel import ResultsPanel # Right Panel - Results

class HiLDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("HiL Test Automation Dashboard - Alpha v0.1")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Create main container
        self.create_header()
        self.create_main_panels()

    def on_run_tests(self, config):
        """Callback when Run button is pressed"""
        from mock_test_runner import MockTestRunner
        
        if not hasattr(self, 'test_runner'):
            self.test_runner = MockTestRunner(self.results_panel)
        
        self.test_runner.run_tests(config)
        
    def create_header(self):
        """Top header bar"""
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill='x', padx=10, pady=10)
        header.pack_propagate(False)
        
        # Title
        title = tk.Label(header, text="HiL Test Automation Dashboard", 
                        font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(side='left', padx=20, pady=20)
        
        # Subtitle
        subtitle = tk.Label(header, text="Hardware-in-Loop Pytest Test Suite Manager", 
                           font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle.pack(side='left', padx=5)
        
        # Settings/Help buttons (non-functional in alpha)
        btn_frame = tk.Frame(header, bg='#2c3e50')
        btn_frame.pack(side='right', padx=20)
        
        tk.Button(btn_frame, text="Settings", width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Help", width=10).pack(side='left', padx=5)
    
    def create_main_panels(self):
        """Create left and right panel containers"""
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # LEFT PANEL - Config
        left_panel = tk.LabelFrame(main_container, text="Test Configuration", 
                                   font=('Arial', 12, 'bold'), bg='white', 
                                   relief='solid', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Add config panel (pass dummy callback for now)
        self.config_panel = ConfigPanel(left_panel, self.on_run_tests)
        
        # RIGHT PANEL - Results 
        right_panel = tk.Frame(main_container, bg='white')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Add results panel
        self.results_panel = ResultsPanel(right_panel)


def main():
    root = tk.Tk()
    app = HiLDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()