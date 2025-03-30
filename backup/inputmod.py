import tkinter as tk
from tkinter import ttk

class TaxInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tax Calculator")
        self.root.geometry("500x400")
        
        # Create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames
        self.primary_frame = ttk.Frame(self.notebook)
        self.partner_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.primary_frame, text="Primary")
        self.partner_tab_id = self.notebook.add(self.partner_frame, text="Partner")
        
        # Initialize partner state
        self.has_partner = tk.BooleanVar(value=False)
        self.update_partner_tab()
        
        # Primary tab content
        ttk.Label(self.primary_frame, text="Primary Information", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Checkbutton(
            self.primary_frame,
            text="I have a fiscal partner",
            variable=self.has_partner,
            command=self.update_partner_tab
        ).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Partner tab content
        ttk.Label(self.partner_frame, text="Partner Information", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.partner_frame, text="Partner Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.partner_name_entry = ttk.Entry(self.partner_frame)
        self.partner_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Submit button
        ttk.Button(root, text="Submit Information", command=self.submit).pack(pady=10)
    
    def update_partner_tab(self):
        """Update partner tab state based on checkbox"""
        if self.has_partner.get():
            self.notebook.tab(self.partner_frame, state="normal")  # Use frame, not partner_tab_id
        else:
            self.notebook.tab(self.partner_frame, state="disabled")
            self.notebook.select(self.primary_frame)  # Ensure primary tab is selected

    
    def submit(self):
        if self.has_partner.get():
            print(f"Submitted with partner: {self.partner_name_entry.get()}")
        else:
            print("Submitted without partner")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaxInputApp(root)
    root.mainloop()
