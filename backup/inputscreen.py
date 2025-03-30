import tkinter as tk
from tkinter import ttk, messagebox

class TaxInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inkomsten Belasting  Input")
        
        # Initialize partner toggle variable
        self.has_partner = tk.BooleanVar(value=False)
        
        # Create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create all frames first
        self.general_frame = ttk.Frame(self.notebook)
        self.primary_frame = ttk.Frame(self.notebook)
        self.partner_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook (store the frame references)
        self.notebook.add(self.general_frame, text="Algemeen")
        self.notebook.add(self.primary_frame, text="Primair")
        self.notebook.add(self.partner_frame, text="Partner", state="disabled")  # Disabled initially
        
        # Build all tabs
        self.create_general_tab()
        self.create_primary_tab()
        self.create_partner_tab()
        
        # Bind partner toggle
        self.has_partner.trace_add('write', lambda *_: self.update_partner_tab())
        
        # Submit button
        ttk.Button(root, text="Submit", command=self.submit_data).pack(pady=10)
        
        # Initialize data structure
        self.input_data = {
            "primary": {},
            "partner": {},
            "programsetting": {}
        }
    
    def create_general_tab(self):
        """General information tab"""
        ttk.Label(self.general_frame, text="Database Path:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.db_path = ttk.Entry(self.general_frame)
        self.db_path.grid(row=0, column=1, padx=5, pady=5)
        self.db_path.insert(0, "mijn_belastingen.db")
        
        ttk.Label(self.general_frame, text="Belasting Jaar:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.year = ttk.Combobox(self.general_frame, values=["2024", "2023", "2022","2021","2020"])
        #self.year = ttk.Entry(self.general_frame)
        self.year.grid(row=1, column=1, padx=5, pady=5)
        self.year.current(0)
        
        # Box 3 assets
        ttk.Label(self.general_frame, text="Box 3 deel", font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=5)
        
        fields = [
            ("Spaargeld:", "spaargeld", "100"),
            ("Beleggingen:", "belegging", "0"),
            ("Ontroeren goed:", "ontroerend", "0"),
            ("WOZ Waarde:", "WOZ_Waarde", "0"),
            ("Schuld box1:", "schuld", "0"),
            ("Ingehouden dividend:", "divident", "0"),
            ("Aftrek Eigen woning:", "AftrekEW", "0")
        ]
        
        for i, (label, attr, default) in enumerate(fields, start=3):
            ttk.Label(self.general_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            setattr(self, attr, ttk.Entry(self.general_frame))
            getattr(self, attr).grid(row=i, column=1, padx=5, pady=5)
            getattr(self, attr).insert(0, default)
        
        # Program settings
        ttk.Label(self.general_frame, text="Program Mode:").grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode = ttk.Combobox(self.general_frame, values=["Normaal", "Bereken optimale verdeling"])
        self.mode.grid(row=10, column=1, padx=5, pady=5)
        self.mode.current(0)
    
    def create_primary_tab(self):
        """Primary taxpayer tab"""
        ttk.Label(self.primary_frame, text="Naam:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.primary_naam = ttk.Entry(self.primary_frame)
        self.primary_naam.grid(row=0, column=1, padx=5, pady=5)
        self.primary_naam.insert(0, "naam")
        
        # Partner checkbox
        ttk.Label(self.primary_frame, text="Heeft Partner:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(
            self.primary_frame,
            variable=self.has_partner
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Other primary fields
        fields = [
            ("AOW Status:", "primary_aow", ["No AOW", "AOW after 1946", "AOW before 1946"], 0),
            ("Inkomen uit Arbeid:", "primary_inkomen", "0"),
            ("Pensioen/Uitkering:", "primary_pensioen", "0"),
            ("Box 1 Uw Deel:", "primary_deel_box1", "1"),
            ("Box 3 Uw Deel:", "primary_deel_box3", "1"),
            ("Dividend Uw deel:", "primary_deel_div", "1"),
            ("Ingehouden loonheffing:", "primary_al_ingehouden", "0"),
            ("Betaald voorlopige belasting:", "primary_voorlopige_aanslag", "0")
        ]
        
        for i, (label, attr, *rest) in enumerate(fields, start=2):
            ttk.Label(self.primary_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            if isinstance(rest[0], list):  # Combobox
                setattr(self, attr, ttk.Combobox(self.primary_frame, values=rest[0]))
                getattr(self, attr).current(rest[1])
            else:  # Entry
                setattr(self, attr, ttk.Entry(self.primary_frame))
                getattr(self, attr).insert(0, rest[0])
            getattr(self, attr).grid(row=i, column=1, padx=5, pady=5)
    
    def create_partner_tab(self):
        """Partner tab (initially disabled)"""
        ttk.Label(self.partner_frame, text="Naam:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.partner_naam = ttk.Entry(self.partner_frame)
        self.partner_naam.grid(row=0, column=1, padx=5, pady=5)
        self.partner_naam.insert(0, "Persoon 2")
        
        # Partner fields
        fields = [
            ("AOW Status:", "partner_aow", ["No AOW", "AOW after 1946", "AOW before 1946"], 1),
            ("Inkomen uit Arbeid:", "partner_inkomen", "0"),
            ("Pensioen/Uitkering:", "partner_pensioen", "0"),
            ("Ingehouden loonheffing:", "partner_al_ingehouden", "0"),
            ("Betaald voorlopige belasting:", "partner_voorlopige_aanslag", "0")
        ]
        
        for i, (label, attr, *rest) in enumerate(fields, start=1):
            ttk.Label(self.partner_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            if isinstance(rest[0], list):  # Combobox
                setattr(self, attr, ttk.Combobox(self.partner_frame, values=rest[0]))
                getattr(self, attr).current(rest[1])
            else:  # Entry
                setattr(self, attr, ttk.Entry(self.partner_frame))
                getattr(self, attr).insert(0, rest[0])
            getattr(self, attr).grid(row=i, column=1, padx=5, pady=5)
    
    def update_partner_tab(self):
        """Update partner tab state based on checkbox (THE FIXED VERSION)"""
        new_state = "normal" if self.has_partner.get() else "disabled"
        self.notebook.tab(self.partner_frame, state=new_state)
        
        # Switch to primary tab if disabling partner
        if not self.has_partner.get():
            self.notebook.select(self.primary_frame)
    
    def submit_data(self):
        """Collect all input data"""
        try:
            # General data
            self.input_data.update({
                "opslagnaam": "belasting",
                "db_path": self.db_path.get(),
                "year": int(self.year.get()),
                "AftrekEW": float(self.AftrekEW.get()),
                "spaargeld": float(self.spaargeld.get()),
                "belegging": float(self.belegging.get()),
                "ontroerend": float(self.ontroerend.get()),
                "WOZ_Waarde": float(self.WOZ_Waarde.get()),
                "schuld": float(self.schuld.get()),
                "divident": float(self.divident.get()),
                "primary": {
                    "naam": self.primary_naam.get(),
                    "aow_er": self.primary_aow.current(),
                    "heeft_partner": self.has_partner.get(),
                    "Inkomen": float(self.primary_inkomen.get()),
                    "Pensioen": float(self.primary_pensioen.get()),
                    "deel_box1": float(self.primary_deel_box1.get()),
                    "deel_box3": float(self.primary_deel_box3.get()),
                    "deel_div": float(self.primary_deel_div.get()),
                    "al_ingehouden": float(self.primary_al_ingehouden.get()),
                    "voorlopige_aanslag": float(self.primary_voorlopige_aanslag.get())
                },
                "programsetting": {
                    "mode": self.mode.current() + 1  # +1 because combobox starts at 0
                }
            })
            
            # Partner data if applicable
            if self.has_partner.get():
                self.input_data["partner"] = {
                    "naam": self.partner_naam.get(),
                    "aow_er": self.partner_aow.current(),
                    "heeft_partner": True,
                    "Inkomen": float(self.partner_inkomen.get()),
                    "Pensioen": float(self.partner_pensioen.get()),
                    "al_ingehouden": float(self.partner_al_ingehouden.get()),
                    "voorlopige_aanslag": float(self.partner_voorlopige_aanslag.get()),
                    # Calculated shares
                    "deel_box1": 1 - self.input_data["primary"]["deel_box1"],
                    "deel_box3": 1 - self.input_data["primary"]["deel_box3"],
                    "deel_div": 1 - self.input_data["primary"]["deel_div"]
                }
            
            messagebox.showinfo("Success", "Data collected successfully!")
            print(self.input_data)  # For debugging
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input:\n{str(e)}")

# Your existing check_input function would be called here if needed
def check_input(data):
    """Validate and enforce dependencies in input data."""

    # Ensure that if primary has a partner, partner data is provided
    if data["primary"]["heeft_partner"]:
        # Primary heeft partner
        if "partner" not in data:
            raise ValueError("Partner data is required when 'heeft_partner' is True.")   
        
        # Enforce deel_box1 dependency
        if "deel_box1" in data["primary"]:
            data["partner"]["deel_box1"] = 1 - data["primary"]["deel_box1"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_box1"] = 1.0
            data["partner"]["deel_box1"] = 0.0

        # Enforce deel_box3 dependency
        if "deel_box3" in data["primary"]:
            data["partner"]["deel_box3"] = 1 - data["primary"]["deel_box3"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_box3"] = 1.0
            data["partner"]["deel_box3"] = 0.0

        # Enforce deel_box3 divident dependency
        if "deel_div" in data["primary"]:
            data["partner"]["deel_div"] = 1 - data["primary"]["deel_div"]
        else:
            # Default to 1 for primary and 1 for partner
            data["primary"]["deel_div"] = 1.0
            data["partner"]["deel_div"] = 0.0
    else: 
        # Geen partner
        data["primary"]["deel_box1"] = 1.0
        data["primary"]["deel_box3"] = 1.0
        data["primary"]["deel_div"] = 1.0

    return data

if __name__ == "__main__":
    root = tk.Tk()
    app = TaxInputApp(root)
    root.mainloop()