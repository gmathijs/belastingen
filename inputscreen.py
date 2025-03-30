""" Start of the belasting calculation GUI"""
# pylint: disable=no-member
# pylint: disable=unsubscriptable-object
# pylint: disable=broad-exception-caught
# pylint: disable=redefined-outer-name
# pylint: disable=trailing-whitespace
# pylint: disable=line-too-long

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

# Start of the standard class 

class TaxInputApp:
    """ Clas belastingen Nederland"""
    def __init__(self, root):
        # Initialize all widgets as None first
        self.primary_aow = None
        self.partner_aow = None
        # Add all other dynamically created widgets here
        self.primary_naam = None
        self.partner_naam = None

        self.filename = "belasting"

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

    def load_csv_data(self):
        """Load input data from CSV file"""
        
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
            # Safely get widgets with existence checks
            if hasattr(self, 'primary_aow') and self.primary_aow:
                aow_index = input_data['primary'].get('aow_er', 0)
                if 0 <= aow_index < len(self.primary_aow['values']):
                    self.primary_aow.current(aow_index)
            
            # Partner AOW
            if (input_data['primary'].get('heeft_partner', False) and 
                hasattr(self, 'partner_aow') and 
                self.partner_aow):
                partner_aow_index = input_data['partner'].get('aow_er', 1)
                if 0 <= partner_aow_index < len(self.partner_aow['values']):
                    self.partner_aow.current(partner_aow_index)
            
            # Numeric fields with validation
            numeric_fields = {
                'primary': ['inkomen', 'pensioen', 'deel_box1', 'deel_box3', 
                        'deel_div', 'al_ingehouden', 'voorlopige_aanslag'],
                'partner': ['inkomen', 'pensioen', 'al_ingehouden', 'voorlopige_aanslag']
            }
            
            for person, fields in numeric_fields.items():
                for field in fields:
                    widget_name = f"{person}_{field}"
                    if hasattr(self, widget_name):
                        widget = getattr(self, widget_name)
                        value = str(input_data[person].get(field, '0'))
                        widget.delete(0, tk.END)
                        widget.insert(0, value)
            
            # Update partner tab state
            self.update_partner_tab()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to populate fields:\n{str(e)}")

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

        
    def create_general_tab(self):
        """General information tab"""
        ttk.Label(self.general_frame, text="Database Path:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.db_path = ttk.Entry(self.general_frame)
        self.db_path.grid(row=0, column=1, padx=5, pady=5)
        self.db_path.insert(0, "mijn_belastingen.db")
        ToolTip(self.db_path, "Pathname to the database)")

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
        ttk.Label(self.general_frame, text="Box 3 deel", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, pady=5)
        
        fields = [
            ("Spaargeld:", "spaargeld", "100"),
            ("Beleggingen:", "belegging", "0"),
            ("Ontroeren goed:", "ontroerend", "0"),
            ("WOZ Waarde:", "WOZ_Waarde", "0"),
            ("Schuld box3:", "schuld", "0"),
            ("Ingehouden dividend:", "divident", "0"),
            ("Aftrek Eigen woning:", "AftrekEW", "0")
        ]
        
        for i, (label, attr, default) in enumerate(fields, start=5):
            ttk.Label(self.general_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            setattr(self, attr, ttk.Entry(self.general_frame))
            getattr(self, attr).grid(row=i, column=1, padx=5, pady=5)
            getattr(self, attr).insert(0, default)
        
        # Program settings
        ttk.Label(self.general_frame, text="Program Mode:").grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode = ttk.Combobox(self.general_frame, values=["Normaal", "Bereken optimale verdeling"])
        self.mode.grid(row=12, column=1, padx=5, pady=5)
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

    def handle_output(self, all_results):
        """Handle output display from within the class"""
        #Format and export the Box 3 tax calculation results.

        
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
        
    def submit_data(self):
        """Collect all input data"""
        try:
            # General data
            self.input_data.update({
                "opslagnaam": self.opslagnaam.get(),
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

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Display tooltip on hover"""
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(
            self.tip_window,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padding=(4, 2)
        )
        label.pack()

    def hide_tip(self, event=None):
        """Destroy tooltip"""
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None



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








def get_screen_dimensions(root):
    """ Calculate screen dimensions"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height



if __name__ == "__main__":
    root = tk.Tk()
    
    # Position main window on left
    screen_width, screen_height = get_screen_dimensions(root)
    window_width = int(screen_width * 0.45)  # 45% of screen width
    window_height = int(screen_height * 0.8)  # 80% of screen height
    
    root.geometry(f"{window_width}x{window_height}+0+0")  # X=0 (far left)
    app = TaxInputApp(root)
    root.mainloop()
