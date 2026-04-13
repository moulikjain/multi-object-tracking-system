import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import sys

class TrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Object Tracker GUI")
        self.root.geometry("600x450")
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        self._build_ui()

    def _build_ui(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.root, text="Step 1: Select Input Video", padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Entry(input_frame, textvariable=self.input_file, state="readonly", width=50).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Browse...", command=self._select_input).pack(side="left")

        # Output Section
        output_frame = ttk.LabelFrame(self.root, text="Step 2: Select Output Destination", padding=(10, 10))
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Entry(output_frame, textvariable=self.output_file, state="readonly", width=50).pack(side="left", padx=5)
        ttk.Button(output_frame, text="Save As...", command=self._select_output).pack(side="left")

        # Run Section
        run_frame = ttk.Frame(self.root, padding=(10, 10))
        run_frame.pack(fill="x", padx=10, pady=5)
        
        self.startButton = ttk.Button(run_frame, text="Start Tracker Processing", command=self._start_processing)
        self.startButton.pack(fill="x", ipady=5)

        # Log Section
        log_frame = ttk.LabelFrame(self.root, text="Processing Logs", padding=(10, 10))
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, state="disabled", wrap="word", height=10)
        self.log_text.pack(fill="both", expand=True)

    def _select_input(self):
        filepath = filedialog.askopenfilename(
            title="Select Input Video", 
            filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*"))
        )
        if filepath:
            self.input_file.set(filepath)

    def _select_output(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Output Video As",
            defaultextension=".mp4",
            filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*"))
        )
        if filepath:
            self.output_file.set(filepath)

    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def _start_processing(self):
        if not self.input_file.get() or not self.output_file.get():
            messagebox.showwarning("Missing Files", "Please select both an input file and an output destination.")
            return
        
        self.startButton.config(state="disabled")
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        
        self.log_message("Initializing tracking pipeline...\n")
        
        # Start the processing in a background thread so UI doesn't freeze
        processing_thread = threading.Thread(target=self._run_main_script)
        processing_thread.daemon = True
        processing_thread.start()

    def _run_main_script(self):
        # Determine the python executable to use
        # Use python from the venv if active, otherwise fallback to standard system python.
        python_exe = sys.executable 
        
        command = [
            python_exe, "main.py", 
            "--input", self.input_file.get(), 
            "--output", self.output_file.get()
        ]
        
        try:
            # We run the command and stream the output continuously
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ''):
                self.log_message(line)
                
            process.stdout.close()
            process.wait()
            
            self.log_message(f"\nProcessing Complete! (Exit Code: {process.returncode})\n")
            if process.returncode == 0:
                messagebox.showinfo("Success", f"Video has been successfully processed and saved to:\n{self.output_file.get()}")
            else:
                messagebox.showerror("Error", "An error occurred during processing. Check logs.")
                
        except Exception as e:
            self.log_message(f"\nFailed to launch process: {str(e)}\n")
            messagebox.showerror("Execution Error", str(e))
        finally:
            self.startButton.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    # Use standard theme wrapper if available
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
        
    app = TrackerGUI(root)
    root.mainloop()
