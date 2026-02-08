"""
Configuration Manager - Handles the saving/loading of test configurations
"""

import json
import os
from datetime import datetime
from tkinter import messagebox, filedialog


class ConfigManager:
    def __init__(self):
        self.config_dir = "configs"
        self._ensure_config_directory()
    
    def _ensure_config_directory(self):
        """Create configs directory if it doesn't exist"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def save_config(self, config_data, filename=None):
        """Save configuration to JSON file"""
        try:
            if filename is None:
                # Ask user for filename
                filename = filedialog.asksaveasfilename(
                    initialdir=self.config_dir,
                    title="Save Configuration",
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                
                if not filename:  # User cancelled
                    return False
            
            # Add metadata
            config_with_meta = {
                'saved_at': datetime.now().isoformat(),
                'version': 'beta-1.0',
                'config': config_data
            }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(config_with_meta, f, indent=4)
            
            messagebox.showinfo("Success", f"Configuration saved to:\n{os.path.basename(filename)}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
            return False
    
    def load_config(self, filename=None):
        """Load configuration from JSON file"""
        try:
            if filename is None:
                # Ask user to select file
                filename = filedialog.askopenfilename(
                    initialdir=self.config_dir,
                    title="Load Configuration",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                
                if not filename:  # User cancelled
                    return None
            
            # Read from file
            with open(filename, 'r') as f:
                config_with_meta = json.load(f)
            
            # Extract config data
            config_data = config_with_meta.get('config', config_with_meta)
            
            messagebox.showinfo("Success", f"Configuration loaded from:\n{os.path.basename(filename)}")
            return config_data
            
        except FileNotFoundError:
            messagebox.showerror("Error", "Configuration file not found!")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid configuration file format!")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
            return None
    
    def get_saved_configs(self):
        """Get list of saved configuration files"""
        try:
            configs = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
            return sorted(configs, reverse=True)  # Most recent first
        except:
            return []
    
    def delete_config(self, filename):
        """Delete a configuration file"""
        try:
            filepath = os.path.join(self.config_dir, filename)
            os.remove(filepath)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete configuration:\n{str(e)}")
            return False