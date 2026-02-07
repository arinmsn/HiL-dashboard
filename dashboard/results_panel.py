"""
Results Panel - Right side of dashboard
Contains status bar, test results summary, results table, and live log viewer
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ResultsPanel:
    def __init__(self, parent):
        self.parent = parent
        
        # Results data
        self.test_results = []
        self.stats = {'total': 0, 'passed': 0, 'failed': 0, 'duration': '0:00'}
        
        self.build_panel()
    
    def build_panel(self):
        """Build all results widgets"""
        
        # Status Bar
        status_frame = tk.Frame(self.parent, bg='#fff3cd', relief='solid', bd=1, height=50)
        status_frame.pack(fill='x', padx=10, pady=10)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Status: Ready", 
                                     font=('Arial', 10, 'bold'), bg='#fff3cd')
        self.status_label.pack(side='left', padx=10, pady=10)
        
        tk.Label(status_frame, text="Last Run: Never", 
                font=('Arial', 9), bg='#fff3cd', fg='gray').pack(side='left', padx=10)
        
        # Export buttons (non-functional in alpha)
        btn_frame = tk.Frame(status_frame, bg='#fff3cd')
        btn_frame.pack(side='right', padx=10)
        
        tk.Button(btn_frame, text="📊 View Report", 
                 command=lambda: messagebox.showinfo("Info", "Report feature coming in Beta")).pack(side='left', padx=2)
        tk.Button(btn_frame, text="📥 Export JUnit XML",
                 command=lambda: messagebox.showinfo("Info", "Export feature coming in Beta")).pack(side='left', padx=2)
        
        # Test Results Summary
        summary_frame = tk.LabelFrame(self.parent, text="Test Results Summary", 
                                     font=('Arial', 11, 'bold'), bg='white', 
                                     relief='solid', bd=2, padx=10, pady=10)
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        stats_container = tk.Frame(summary_frame, bg='white')
        stats_container.pack(fill='x', pady=5)
        
        # Stats boxes
        self.stat_widgets = {}
        stats_info = [
            ('total', 'Total Tests', '#ecf0f1'),
            ('passed', 'Passed', '#d5f4e6'),
            ('failed', 'Failed', '#fadbd8'),
            ('duration', 'Duration', '#ecf0f1')
        ]
        
        for i, (key, label, color) in enumerate(stats_info):
            stat_box = tk.Frame(stats_container, bg=color, relief='solid', bd=2)
            stat_box.pack(side='left', fill='both', expand=True, padx=5)
            
            value_label = tk.Label(stat_box, text='0' if key != 'duration' else '0:00', 
                                  font=('Arial', 20, 'bold'), bg=color)
            value_label.pack(pady=(10, 0))
            
            tk.Label(stat_box, text=label, font=('Arial', 9), bg=color, fg='gray').pack(pady=(0, 10))
            
            self.stat_widgets[key] = value_label
        
        # Results Table
        table_frame = tk.LabelFrame(self.parent, text="Test Results Table", 
                                   font=('Arial', 11, 'bold'), bg='white', 
                                   relief='solid', bd=2)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ('test', 'status', 'duration')
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=6)
        
        self.results_tree.heading('test', text='Test Name')
        self.results_tree.heading('status', text='Status')
        self.results_tree.heading('duration', text='Duration')
        
        self.results_tree.column('test', width=300)
        self.results_tree.column('status', width=100)
        self.results_tree.column('duration', width=100)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        # Live Log Viewer
        log_frame = tk.LabelFrame(self.parent, text="Live Test Execution Log", 
                                 font=('Arial', 11, 'bold'), bg='white', 
                                 relief='solid', bd=2)
        log_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Log text widget
        self.log_text = tk.Text(log_frame, height=10, bg='#0c0c0c', fg='#00ff00', 
                               font=('Courier', 9), wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        log_scroll = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # Initial log message
        self.log_text.insert('end', '[SYSTEM] Dashboard initialized. Ready to run tests.\n')
        self.log_text.config(state='disabled')
    
    def update_status(self, status_text):
        """Update status bar"""
        self.status_label.config(text=f"Status: {status_text}")
    
    def update_stats(self, total, passed, failed, duration):
        """Update summary statistics"""
        self.stat_widgets['total'].config(text=str(total))
        self.stat_widgets['passed'].config(text=str(passed))
        self.stat_widgets['failed'].config(text=str(failed))
        self.stat_widgets['duration'].config(text=duration)
    
    def add_test_result(self, test_name, status, duration):
        """Add a row to results table"""
        tag = 'passed' if status == 'PASSED' else 'failed'
        self.results_tree.insert('', 'end', values=(test_name, status, duration), tags=(tag,))
        
        # Color coding
        self.results_tree.tag_configure('passed', foreground='#27ae60')
        self.results_tree.tag_configure('failed', foreground='#e74c3c')
    
    def clear_results(self):
        """Clear all results"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.update_stats(0, 0, 0, '0:00')
    
    def add_log(self, message):
        """Add message to log viewer"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')  # Auto-scroll to bottom
        self.log_text.config(state='disabled')