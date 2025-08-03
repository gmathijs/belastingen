""" Start of the belasting calculation GUI"""
# pylint: disable=no-member
# pylint: disable=unsubscriptable-object
# pylint: disable=broad-exception-caught
# pylint: disable=redefined-outer-name
# pylint: disable=trailing-whitespace
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring

# CTRL K J = unfold CTRL K O = Fold

# Standard library
import os
import threading

# tkinter 
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Local Application
from belastingen import belastingen
from functions_output import (format_table_all, 
                              merge_data, 
                              format_table_totaal
                              )
from save_input import (read_input_from_csv, 
                        write_input_to_csv
                        )
from functions_graphs_tabbed import create_tabbed_graphs

class TaxInputApp:
    """
    Opent het GUI window om belasting gegevens in te vullen.
    Vanuit het GUI window wordt de berekening gestart.
    """
    # ------------------
    # Initialization
    # ------------------
    def __init__(self, root):
        # Initialize all widgets as None first
        self.primary_aow = None
        self.partner_aow = None
        self.primary_naam = None
        self.partner_naam = None

        self.filename = "belasting"

        self.root = root
        self.setup_validation()  # Initialize validation system
        self.root.title("Inkomsten Belasting  Input")
        

        # Initialize partner toggle variable
        self.primary_heeft_partner = tk.BooleanVar(value=False)
        
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
        #self.primary_heeft_partner.trace_add('write', lambda *_: self.update_partner_tab())
        
        # Initialize data structure
        self.input_data = {
            "primary": {},
            "partner": {},
            "programsetting": {}
        }


        self.calculating = False
        self.progress_label = ttk.Label(root, text="")
        self.progress_label.pack(pady=5)

        # Create button frame at bottom
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10, fill=tk.X)
        
        # Add buttons with consistent styling
        btn_style = {'width': 12, 'padding': (5, 2)}
        
        ttk.Button(
            button_frame, 
            text="Load Input", 
            command=self.load_csv_data,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Save Input", 
            command=self.save_current_input,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.submit_button = ttk.Button(
            button_frame, 
            text="Calculate", 
            command=self.start_calculation,
            style='Accent.TButton',  # Make calculate button stand out
            **btn_style
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Quit", 
            command=self.quit_program,
            **btn_style
        ).pack(side=tk.RIGHT, padx=5)

        # Run audit last
        self.audit_widget_names() 

    def audit_widget_names(self):
        """Print all widget attributes and their types"""
        print("\n=== WIDGET AUDIT ===")
        for name, obj in vars(self).items():
            if isinstance(obj, (tk.Widget, ttk.Widget, tk.Variable)):
                print(f"{name.ljust(25)} {str(type(obj)).split('.')[-1]}")

    def load_csv_data(self):
        """
            File Dialog Asks the user to give a Input CSV file 
            Calls: Read_input_from_csv, populate_fields

        """
        
        file_path = filedialog.askopenfilename(
            title="Select Input CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        
        if file_path:
            try:
                input_data = read_input_from_csv(file_path)
                self.populate_fields(input_data)
                messagebox.showinfo(
                    "Success", 
                    f"Loaded input from:\n{file_path}\n\n"
                    "Please verify all values and click Calculate when ready."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV:\n{str(e)}")

    def populate_fields(self, input_data):
        """Populate GUI fields with data from dictionary"""
        try:
            # Debug input
            print("Input data received:", input_data.keys())
            if 'primary' in input_data:
                print("Primary data:", input_data['primary'].keys())
            
            # ===== General Tab Fields =====
            general_fields = {
                'db_path': 'db_path',  
                'opslagnaam': 'opslagnaam',                          # Common alternative name
                'year': 'year',
                'aftrek_eigenwoning': 'aftrek_eigenwoning',
                'spaargeld': 'spaargeld',
                'belegging': 'belegging',
                'ontroerend': 'ontroerend',
                'woz_waarde': 'woz_waarde',
                'schuld': 'schuld',
                'dividend': 'dividend'
            }
            
            for field, widget_name in general_fields.items():
                if hasattr(self, widget_name):
                    widget = getattr(self, widget_name)
                    value = str(input_data.get(field, ''))
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
                    print(f"Set {widget_name} to {value}")  # Debug
                else:
                    print(f"Widget {widget_name} not found")  # Debug

            # ===== Primary Tab Fields =====
            # AOW status
            if hasattr(self, 'primary_aow') and self.primary_aow:
                aow_index = input_data['primary'].get('aow_er', 0)
                self.primary_aow.current(aow_index)
                print(f"Set AOW to index {aow_index}")  # Debug
            
        # Partner checkbox - using the correct variable name
            if hasattr(self, 'primary_heeft_partner'):
                # Get the value from input data (default to False if not found)
                partner_status = input_data['primary'].get('heeft_partner', False)
                
                # Set the checkbox value
                self.primary_heeft_partner.set(partner_status)
                print(f"DEBUG: Partner checkbox set to {partner_status}")
                
                # Force GUI update
                self.update_partner_tab()
                
                # If partner exists, make sure tab is enabled immediately
                if partner_status and hasattr(self, 'partner_tab'):
                    self.notebook.tab(self.partner_tab, state='normal')

            # Primary fields with case-insensitive fallback
            primary_mappings = {
                'Naam': 'primary_naam',
                'Inkomen': 'primary_inkomen',
                'Pensioen': 'primary_pensioen',
                'deel_box1': 'primary_deel_box1',
                'deel_box3': 'primary_deel_box3',
                'deel_div': 'primary_deel_div',
                'al_ingehouden': 'primary_al_ingehouden',
                'voorlopige_aanslag': 'primary_voorlopige_aanslag'
            }
            
            for field, widget_name in primary_mappings.items():
                if hasattr(self, widget_name):
                    value = input_data['primary'].get(field) or input_data['primary'].get(field.lower(), '')
                    widget = getattr(self, widget_name)
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
                    print(f"Set {widget_name} to {value}")  # Debug

            # ===== Partner Tab Fields =====
            # ===== Partner Checkbox =====
            if hasattr(self, 'primary_heeft_partner'):
                # Get partner status - default to False if not found
                heeft_partner = input_data['primary'].get('heeft_partner', False)
                self.primary_heeft_partner.set(heeft_partner)
                print(f"DEBUG: Partner checkbox set to {heeft_partner}")

                # ===== Critical Fix =====
                # Immediately process partner data if exists
                if heeft_partner and 'partner' in input_data:
                    # Force partner tab to be visible first
                    if hasattr(self, 'partner_tab'):
                        self.notebook.tab(self.partner_tab, state='normal')
                    
                    # Now populate partner fields
                    partner_mappings = {
                        'naam': 'partner_naam',
                        'aow_er': 'partner_aow',
                        'Inkomen': 'partner_inkomen',
                        'Pensioen': 'partner_pensioen',
                        'al_ingehouden': 'partner_al_ingehouden',
                        'voorlopige_aanslag': 'partner_voorlopige_aanslag',
                        'deel_box1': 'partner_deel_box1',
                        'deel_box3': 'partner_deel_box3',
                        'deel_div': 'partner_deel_div'
                    }

                    for field, widget_name in partner_mappings.items():
                        if hasattr(self, widget_name):
                            widget = getattr(self, widget_name)
                            value = str(input_data['partner'].get(field, ''))
                            
                            if isinstance(widget, ttk.Combobox):
                                widget.set(value)
                            else:
                                widget.delete(0, tk.END)
                                widget.insert(0, value)
                            print(f"Set {widget_name} to {value}")

            # Force final GUI update
            self.update_partner_tab()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to populate fields:\n{str(e)}")
            raise


    def start_calculation(self):
        """Start the tax calculation process"""
        if not self.calculating:
            self.calculating = True
            self.submit_button.config(state=tk.DISABLED)
            self.progress_label.config(text="Calculating...")

            self.delete_output(self.filename)
            
            # Get the input data
            try:
                input_data = self.submit_data()  # This collects data but doesn't close window
                if input_data:
                    # Start calculation in a separate thread

                    threading.Thread(
                        target=self.run_calculation,
                        args=(input_data,),
                        daemon=True
                    ).start()
            except Exception as e:
                self.calculating = False
                self.submit_button.config(state=tk.NORMAL)
                messagebox.showerror("Error", f"Data collection failed:\n{str(e)}")

    def run_calculation(self, input_data):
        """Run the calculation and update UI when done"""
        try:
            # Run the calculation
            result = belastingen(input_data)
            
            # Update UI when done
            self.root.after(0, self.calculation_done, result)
        except Exception as e:
            self.root.after(0, self.calculation_failed, str(e))
        
    def calculation_done(self, result):
        """Handle successful calculation"""
        self.calculating = False
        self.submit_button.config(state=tk.NORMAL)
        self.progress_label.config(text="Calculation complete!")
        
        # Handle the output display
        self.handle_output(result)
        
        # Optional: show summary in messagebox
        # total = result['totaal']['aanslag']

        #messagebox.showinfo(
        #   "Calculation Complete",
        #   f"Tax calculation finished!\nTotal amount: €{total:,.2f}"
        #)
        
    def calculation_failed(self, error):
        """Handle calculation errors"""
        self.calculating = False
        self.submit_button.config(state=tk.NORMAL)
        self.progress_label.config(text="Calculation failed")
        messagebox.showerror("Error", f"Calculation failed:\n{error}")

    def delete_output(self, filename):
        """ If filename is the default name then clean up the existing .txt files"""
        # Check if file exists and find the next available number
        if filename == self.filename:
            counter = 1
            basename = filename 
            filename = basename+".txt"
            while os.path.exists(filename):
                os.remove(filename)
                filename = f"{basename}_{counter}.txt"
                counter += 1
    # ------------------
    # Create Window Tabs
    # ------------------        
    def create_general_tab(self):
        """General information tab"""
        ttk.Label(self.general_frame, text="Database Path:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.db_path = ttk.Entry(self.general_frame)
        self.db_path.grid(row=0, column=1, padx=5, pady=5)
        self.db_path.insert(0, "mijn_belastingen.db")
        ToolTip(self.db_path, "Pathname to the database")

        ttk.Label(self.general_frame, text="Opslagnaam:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.opslagnaam = ttk.Entry(self.general_frame)
        self.opslagnaam.grid(row=1, column=1, padx=5, pady=5)
        self.opslagnaam.insert(0, self.filename)
            
        ttk.Label(self.general_frame, text="Belasting Jaar:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.year = ttk.Combobox(self.general_frame, values=["2024", "2023", "2022","2021","2020"])
        #self.year = ttk.Entry(self.general_frame)
        self.year.grid(row=3, column=1, padx=5, pady=5)
        self.year.current(0)
        
        # Box 3 assets
        ttk.Label(self.general_frame, text="Opgaven Box 3 ", font=('Arial', 14, 'bold')).grid(row=4, column=0, columnspan=2, pady=5)
        
        fields = [
            ("Spaargeld:", "spaargeld", "100", "Opgeteld spaargeld op alle rekeningen"),
            ("Beleggingen:", "belegging", "0", "Totaal uitstaande beleggingen op 1 Januari (zie jaaropgaven)"),
            ("Ontroeren goed:", "ontroerend", "0", "Waarde ontroerend goed, vakantie huis etc."),
            ("WOZ Waarde:", "woz_waarde", "0", "WOZ waarde peiling 1 januari van het belastingjaar"),
            ("Schuld box3:", "schuld", "0", "Aftrekbare Schulden in box 3 check de belasting website"),
            ("Ingehouden dividend:", "dividend", "0", "Totaal ingehouden dividend"),
            ("Aftrek Eigen woning:", "aftrek_eigenwoning", "0", "Aftrekbare kosten eigenwoning, betaalde rente, afsluitkosten")
        ]
        
        for i, (label, attr, default, tooltip) in enumerate(fields, start=5):
            ttk.Label(self.general_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            setattr(self, attr, ttk.Entry(self.general_frame))
            getattr(self, attr).grid(row=i, column=1, padx=5, pady=5)
            getattr(self, attr).insert(0, default)

            # Create validated entry
            entry = ttk.Entry(
                self.general_frame,
                validate="key",
                validatecommand=self.validate_num_cmd
            )
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, default)
            
            # Bind to show validation status
            entry.bind("<FocusOut>", self.update_validation_style)
            self.update_validation_style(None, entry)  # Initial validation
            
            setattr(self, attr, entry)
            
            # Add tooltip if specified
            #if tooltip:
            #    ToolTip(entry, tooltip)
            
            # Add tooltip if specified
            if tooltip:
                ToolTip(getattr(self, attr), tooltip)
       
        # Program settings
        ttk.Label(self.general_frame, text="Program Mode:").grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        self.programsetting_mode = ttk.Combobox(self.general_frame, values=["Normaal", "Bereken optimale verdeling","Loop salaris"])
        self.programsetting_mode.grid(row=12, column=1, padx=5, pady=5)
        self.programsetting_mode.current(0)
        
    def create_primary_tab(self):
        """Primary taxpayer tab"""
        # Clear previous widgets if any (safety measure)
        for widget in self.primary_frame.winfo_children():
            widget.destroy()
        
        # Name field
        ttk.Label(self.primary_frame, text="Naam:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.primary_naam = ttk.Entry(self.primary_frame)
        self.primary_naam.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.primary_naam.insert(0, "naam")
        
        # Partner checkbox
        ttk.Label(self.primary_frame, text="Heeft Partner:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(
            self.primary_frame,
            variable=self.primary_heeft_partner,
            command=self.update_partner_tab  # Ensure this is connected
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        
        # Other primary fields with tooltips
        fields = [
            ("AOW Status:", "primary_aow", ["No AOW", "AOW after 1946", "AOW before 1946"], 0, "Selecteer of persoon AOW heeft"),
            ("Inkomen uit Arbeid:", "primary_inkomen", "0", "Totaal Inkomen uit Arbeid"),
            ("Pensioen/Uitkering:", "primary_pensioen", "0", "Pensioen en andere uitkeringen"),
            ("Box 1 Uw Deel:", "primary_deel_box1", "1", "0 - 1 Welk deel van Box1 komt voor jouw rekening"),
            ("Box 3 Uw Deel:", "primary_deel_box3", "1", "0 - 1 Welk deel van Box3 komt voor jouw rekening"),
            ("Dividend Uw deel:", "primary_deel_div", "1", "0 - 1 Welk deel van Dividend komt voor jouw rekening"),
            ("Ingehouden loonheffing:", "primary_al_ingehouden", "0", "Totale ingehouden loonheffing zie jaaropgaven"),
            ("Betaald voorlopige belasting:", "primary_voorlopige_aanslag", "0", "Al betaald via Voorlopige Aanslag")
        ]

        for i, (label, attr, *rest) in enumerate(fields, start=2):
            # Create label
            ttk.Label(self.primary_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Create widget
            if isinstance(rest[0], list):  # Combobox
                widget = ttk.Combobox(self.primary_frame, values=rest[0])
                widget.current(rest[1])
                tooltip_text = rest[2] if len(rest) > 2 else ""
            else:  # Entry field
                # Determine validation type
                if attr in ['primary_deel_box1', 'primary_deel_box3', 'primary_deel_div']:
                    validate_cmd = self.validate_share_cmd
                else:
                    validate_cmd = self.validate_num_cmd
                
                widget = ttk.Entry(
                    self.primary_frame,
                    validate="key",
                    validatecommand=validate_cmd
                )
                widget.insert(0, rest[0])
                tooltip_text = rest[1] if len(rest) > 1 else ""
                
                # Set up validation
                widget.bind("<FocusOut>", lambda e, w=widget: self.update_validation_style(widget=w))
                self.update_validation_style(widget=widget)
            
            # Grid the widget
            widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            setattr(self, attr, widget)
            
            # Add tooltip if specified
            if tooltip_text:
                ToolTip(widget, tooltip_text)
        
        # Configure column weights
        self.primary_frame.columnconfigure(0, weight=1)
        self.primary_frame.columnconfigure(1, weight=3)
            
    def create_partner_tab(self):
        """Partner tab (initially disabled)"""
        # Clear previous widgets if any
        for widget in self.partner_frame.winfo_children():
            widget.destroy()


        ttk.Label(self.partner_frame, text="Naam:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.partner_naam = ttk.Entry(self.partner_frame)
        self.partner_naam.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.partner_naam.insert(0, "Persoon 2")
        
        # Partner fields
        fields = [
            ("AOW Status:", "partner_aow", ["No AOW", "AOW after 1946", "AOW before 1946"], 0, "Selecteer of persoon AOW heeft"),
            ("Inkomen uit Arbeid:", "partner_inkomen", "0","Totaal Inkomen uit Arbeid"),
            ("Pensioen/Uitkering:", "partner_pensioen", "0","Pensioen en andere uitkeringen"),
            ("Ingehouden loonheffing:", "partner_al_ingehouden", "0","Totale ingehouden loonheffing zie jaaropgaven"),
            ("Betaald voorlopige belasting:", "partner_voorlopige_aanslag", "0", "Al betaald via Voorlopige Aanslag")
        ]
        
        for i, (label, attr, *rest) in enumerate(fields, start=1):  # Start at row 1
            ttk.Label(self.partner_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            if isinstance(rest[0], list):  # Combobox
                widget = ttk.Combobox(self.partner_frame, values=rest[0])
                widget.current(rest[1])
                tooltip_text = rest[2] if len(rest) > 2 else ""
            else:  # Entry field
                # Use share validation for deel fields
                validate_cmd = self.validate_num_cmd
                    
                widget = ttk.Entry(
                    self.partner_frame,
                    validate="key",
                    validatecommand=validate_cmd
                )
                widget.insert(0, rest[0])
                tooltip_text = rest[1] if len(rest) > 1 else ""
                
                # Set up validation styling
                widget.bind("<FocusOut>", lambda e, w=widget: self.update_validation_style(widget=w))
                self.update_validation_style(widget=widget)
            
            widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            setattr(self, attr, widget)
            
            if tooltip_text:
                ToolTip(widget, tooltip_text)
        
        # Configure column weights
        self.partner_frame.columnconfigure(0, weight=1)
        self.partner_frame.columnconfigure(1, weight=3)

    def update_partner_tab(self):
        """Update partner tab state based on checkbox (THE FIXED VERSION)"""

        new_state = "normal" if self.primary_heeft_partner.get() else "disabled"
        self.notebook.tab(self.partner_frame, state=new_state)
        
        # Switch to primary tab if disabling partner
        if not self.primary_heeft_partner.get():
            self.notebook.select(self.primary_frame)
    # ------------------
    # Output and  on Screen Handling
    # ------------------
    def handle_output(self, all_results):
        """Handle output display from within the class"""
        #Format and export the Box 3 tax calculation results.

        # Graph Necessary?
        if all_results['input']['programsetting']['programsetting_mode'] ==3: 
            # Dan is er een resultaat deel in all_results
            print("Grafiek kan worden geplaatst")
            # Extract data from the dictionary
            resultaat = all_results['resultaat']
            create_tabbed_graphs(resultaat, self.root)
            #create_grah_income(resultaat)


        
        # Define the file name
        base_name = all_results['input']['opslagnaam']
        filename = f"{base_name}.txt"
        counter = 1

        # Check if file exists and find the next available number
        while os.path.exists(filename):
            filename = f"{base_name}_{counter}.txt"
            counter += 1

        # Extract individual results from the dictionary for the primary 
        input_data = merge_data(all_results['input'],all_results['input']['primary'])

        # Make up the output table 
        table_all_primary = format_table_all(input_data,all_results['primary'])
        print(table_all_primary)
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Primary Person Results:\n")
            file.write(table_all_primary + "\n") 

        # Extract individual results from the dictionary if partner exists 
        if input_data['heeft_partner']:
            input_data = merge_data(all_results['input'],all_results['input']['partner'])

            table_all_partner = format_table_all(input_data,all_results['partner'])
            print(table_all_partner)
            with open(filename, "a", encoding="utf-8") as file:
                file.write("\nPartner Results:\n")
                file.write(table_all_partner + "\n")


        table_totaal = format_table_totaal(all_results)
        print(table_totaal)
        with open(filename, "a", encoding="utf-8") as file:
            file.write(table_totaal + "\n")

        if all_results['input']['programsetting']['programsetting_mode'] != 3: 
            # Show in positioned window
            self.show_results_in_window(filename)

    def show_results_in_window(self, filename):
        """Display results in a window positioned on the right"""
        result_window = tk.Toplevel(self.root)
        
        # Calculate position (right side of screen)
        screen_width = self.root.winfo_screenwidth()
        window_width = int(screen_width * 0.35)
        screen_height = self.root.winfo_screenheight()
        window_height = int(screen_height * 0.85)        
        x_position = screen_width - window_width
        
        result_window.geometry(f"{window_width}x{window_height}+{x_position}+0")
        result_window.title("Tax Calculation Results")
        
        # Add text widget
        text_widget = tk.Text(result_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_window, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.pack(expand=True, fill=tk.BOTH)
        
        # Read and display file contents
        try:
            with open(filename, 'r') as file:
                text_widget.insert(tk.END, file.read())
        except Exception as e:
            text_widget.insert(tk.END, f"Error reading file: {str(e)}")
        
        text_widget.config(state=tk.DISABLED)
    # ------------------
    # Button Actions
    # ------------------
    def submit_data(self):
        """Collect all input data"""
        try:
            # General data
            self.input_data.update({
                "opslagnaam": self.opslagnaam.get(),
                "db_path": self.db_path.get(),
                "year": int(self.year.get()),
                "aftrek_eigenwoning": float(self.aftrek_eigenwoning.get()),
                "spaargeld": float(self.spaargeld.get()),
                "belegging": float(self.belegging.get()),
                "ontroerend": float(self.ontroerend.get()),
                "woz_waarde": float(self.woz_waarde.get()),
                "schuld": float(self.schuld.get()),
                "dividend": float(self.dividend.get()),
                "primary": {
                    "naam": self.primary_naam.get(),
                    "aow_er": self.primary_aow.current(),
                    "heeft_partner": self.primary_heeft_partner.get(),
                    "Inkomen": float(self.primary_inkomen.get()),
                    "Pensioen": float(self.primary_pensioen.get()),
                    "deel_box1": float(self.primary_deel_box1.get()),
                    "deel_box3": float(self.primary_deel_box3.get()),
                    "deel_div": float(self.primary_deel_div.get()),
                    "al_ingehouden": float(self.primary_al_ingehouden.get()),
                    "voorlopige_aanslag": float(self.primary_voorlopige_aanslag.get())
                },
                "programsetting": {
                    "programsetting_mode": self.programsetting_mode.current() + 1  # +1 because combobox starts at 0
                }
            })
            
            # Partner data if applicable
            if self.primary_heeft_partner.get():
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
            
            return self.input_data
                
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input:\n{str(e)}")
        return None

    def save_current_input(self):
        """Save current input values to CSV"""
        
        # Get current data
        input_data = self.submit_data()  # Reuse your existing data collection
        if not input_data:
            return
        
        # Ask for save location
        default_name = f"{input_data['opslagnaam']}.csv"
        file_path = filedialog.asksaveasfilename(
            title="Save Input As",
            initialfile=default_name,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        
        if file_path:
            try:
                write_input_to_csv(input_data, file_path)
                messagebox.showinfo("Success", f"Input saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")

    def quit_program(self):
        """Cleanly exit the application"""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    def add_recent_files_menu(self):
        """Add recent files submenu to File menu"""
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        
        # Add your recent files logic here
        recent_files = self.load_recent_files_list()  # Implement this
        
        for i, file_path in enumerate(recent_files[:5]):  # Show last 5
            filemenu.add_command(
                label=f"{i+1}. {os.path.basename(file_path)}",
                command=lambda f=file_path: self.load_specific_file(f)
            )
        
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
    # ------------------
    # Validation of input
    # ------------------
    def setup_validation(self):
        """Initialize validation system"""
        self.style = ttk.Style()
        self.style.configure("Valid.TEntry", foreground="green")
        self.style.configure("Error.TEntry", foreground="red")
        
        # List of share fields that need 0-1 validation
        self.share_fields = ['primary_deel_box1', 'primary_deel_box3', 'primary_deel_div']
        
        # Create validation commands
        self.validate_num_cmd = (self.root.register(self.validate_number_input), '%P')
        self.validate_share_cmd = (self.root.register(self.validate_share_input), '%P')

    def update_validation_style(self, event=None, widget=None):
        """Update the visual style based on validation status"""
        widget = widget or event.widget
        value = widget.get()
        
        try:
            if value == "":
                widget.configure(style="TEntry")
                return
                
            num = float(value)
            
            # Check if this is a share field by widget name
            widget_name = str(widget)
            is_share_field = any(field in widget_name for field in self.share_fields)
            
            if is_share_field:
                widget.configure(style="Valid.TEntry" if 0 <= num <= 1 else "Error.TEntry")
            else:
                widget.configure(style="Valid.TEntry" if num >= 0 else "Error.TEntry")
                
        except ValueError:
            widget.configure(style="Error.TEntry")

    def validate_share_input(self, new_value):
        """Validate that input is a number between 0 and 1"""
        try:
            if new_value == "":  # Allow empty field temporarily
                return True
                
            num = float(new_value)
            return 0 <= num <= 1  # Only allow numbers between 0 and 1
            
        except ValueError:
            return False

    def validate_number_input(self, new_value):
        """Validate that input is a number >= 0"""
        try:
            if new_value == "":  # Allow empty field temporarily
                return True
                
            # Try converting to float
            num = float(new_value)
            
            # Check if number is >= 0
            return num >= 0
            
        except ValueError:
            return False

    def validate_all_fields(self):
        """Validate all numeric fields before submission"""
        fields = ["spaargeld", "belegging", "ontroerend", "woz_waarde", 
                 "schuld", "dividend", "aftrek_eigenwoning","primary_inkomen","primary_pensioen",
                 "primary_deel_div","primary_al_ingehouden","primary_voorlopige_aanslag",
                 "primary_deel_box1", "primary_deel_box3"]
        

        for field in fields:
            entry = getattr(self, field)
            value = entry.get()
            
            if value == "":
                messagebox.showerror("Error", f"Field {field} cannot be empty")
                entry.focus_set()
                return False
                
            try:
                if float(value) < 0:
                    messagebox.showerror("Error", f"Field {field} must be >= 0")
                    entry.focus_set()
                    return False
            except ValueError:
                messagebox.showerror("Error", f"Field {field} must be a number")
                entry.focus_set()
                return False
                
        return True

class ToolTip:
    """
        Handelt de tooltips af. 
        Bevat de defaults maar geeft ook de mogelijkheden voor 
        persoonlijke aanpassingen
    """
    def __init__(self, widget, text, 
                 bg="#ffffe0", fg="black", 
                 font=("tahoma", "12", "normal"),
                 delay=500, 
                 x_offset=150, y_offset=25,
                 border=1, 
                 justify="left",
                 relief="solid"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.font = font
        self.delay = delay  # in milliseconds
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.border = border
        self.justify = justify
        self.relief = relief
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule_tip)
        self.widget.bind("<Leave>", self.hidetip)
        self.widget.bind("<ButtonPress>", self.hidetip)

    def schedule_tip(self, event):
        self.id = self.widget.after(self.delay, self.showtip)

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        
        # Calculate position
        x = self.widget.winfo_rootx() + self.x_offset
        y = self.widget.winfo_rooty() + self.y_offset
        
        # Create window
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Customize appearance
        label = tk.Label(tw, text=self.text, justify=self.justify,
                      background=self.bg, foreground=self.fg,
                      relief=self.relief, borderwidth=self.border,
                      font=self.font)
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Check Input Data (wordt niet gebruikt vlgs mij)
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

        # Enforce deel_box3 dividend dependency
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

# Afmetingen Computer Scherm
def get_screen_dimensions(root):
    """Bepaalt de afmetingen van het scherm om  ordentelijke 
    invoer en uitvoer schermen te tonen
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

# ------------------------
# Start het hoofdprogramma
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    
    # Position main window on left
    screen_width, screen_height = get_screen_dimensions(root)
    window_width = int(screen_width * 0.45)  # 45% of screen width
    window_height = int(screen_height * 0.8)  # 80% of screen height
    
    root.geometry(f"{window_width}x{window_height}+0+0")  # X=0 (far left)
    app = TaxInputApp(root)
    root.mainloop()
