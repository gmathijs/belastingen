""" 
Advanced Income Analysis Graphs with Interactive Crosshairs
Gaston: Last update 2025-04
"""
# pylint: disable=no-member,unsubscriptable-object,broad-exception-caught
# pylint: disable=redefined-outer-name,trailing-whitespace,line-too-long
# pylint: disable=missing-function-docstring,too-many-locals,invalid-name

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Constants for consistent styling
CROSSHAIR_COLOR = '#FF5722'  # Orange
CROSSHAIR_STYLE = dict(lw=1, ls='--', alpha=0)
ANNOTATION_STYLE = dict(
    xytext=(10, 10),
    textcoords="offset points",
    bbox=dict(
        boxstyle="round,pad=0.3",
        fc="white",  # Solid white background
        ec="#333333",  # Dark gray border
        lw=1,
        alpha=0.95  # Slightly transparent
    ),
    fontsize=9,
    fontfamily='sans-serif',
    fontweight='normal',
    color='#333333'  # Dark gray text
)

def clean_currency(value):
    """Convert '€1,000' → 1000.0"""
    try:
        return float(value.replace('€','').replace(',',''))
    except (ValueError, AttributeError):
        return 0.0

def add_crosshair(fig, ax, lines):
    """Advanced crosshair snapping for multiple lines with smart labeling."""
    # Create crosshairs
    hline = ax.axhline(color=CROSSHAIR_COLOR, **CROSSHAIR_STYLE)
    vline = ax.axvline(color=CROSSHAIR_COLOR, **CROSSHAIR_STYLE)
    annot = ax.annotate("", xy=(0,0), **ANNOTATION_STYLE)
    annot.set_visible(False)

    def on_motion(event):
        if event.inaxes != ax:
            hline.set_alpha(0)
            vline.set_alpha(0)
            annot.set_visible(False)
            fig.canvas.draw_idle()
            return

        # Performance optimization for large datasets
        xlim = ax.get_xlim()
        if len(lines[0].get_xdata()) > 100 and not (xlim[0] <= event.xdata <= xlim[1]):
            return

        # Find closest point across all lines
        min_dist = float('inf')
        best_point = None
        
        for line in lines:
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            idx = np.argmin(np.abs(xdata - event.xdata))
            x, y = xdata[idx], ydata[idx]
            dist = np.sqrt((event.xdata - x)**2 + (event.ydata - y)**2)
            
            if dist < min_dist:
                min_dist = dist
                best_point = (x, y, line.get_label())

        # Update display if valid point found
        if best_point and min_dist < (0.05 * (xlim[1] - xlim[0])):  # 5% threshold
            x, y, label = best_point
            hline.set_ydata([y, y])
            vline.set_xdata([x, x])
            hline.set_alpha(0.7)
            vline.set_alpha(0.7)
            
            # Smart annotation positioning
            x_pos = x + 0.02*(xlim[1] - xlim[0])
            y_pos = y + 0.02*(ax.get_ylim()[1] - ax.get_ylim()[0])
            annot.xy = (x_pos, y_pos)
            annot.set_text(f"{label}\nX: €{x:,.0f}\nY: €{y:,.0f}")
            annot.set_visible(True)
        else:
            annot.set_visible(False)
            
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    return hline, vline, annot

def create_tabbed_graphs(resultaat, master_window):
    """Main function to create the tabbed analysis interface."""
    # Data extraction
     #       arbeidskorting =  all_results['primary'] ['box1'] ['arbeidskorting']  
     #       ouderenkorting = all_results['primary'] ['box1'] ['ouderenkorting']           



    data_keys = ['inkomen_arbeid', 'box1_loonheffing', 'totale_aanslag', 
                 'premies_volksverz', 'arbeidskorting', 'ouderenkorting','heffingskorting', 'kortingentotaal','aanslag']
    incomes, box1_tax, box1_total, premies, arbeidskorting, ouderenkorting, heffingskorting, kortingen ,aanslag = (
        [clean_currency(row[key]) for row in resultaat] for key in data_keys
    )

    # Window management
    if hasattr(master_window, 'graph_window'):
        try:
            if master_window.graph_window.winfo_exists():
                master_window.graph_window.lift()
                return
        except (tk.TclError, AttributeError):
            pass

    master_window.graph_window = tk.Toplevel(master_window)
    gw = master_window.graph_window
    gw.title("Income Analysis Dashboard")
    gw.geometry("1100x850")
    gw.transient(master_window)

    def on_closing():
        if hasattr(master_window, 'graph_window'):
            master_window.graph_window = None
        gw.destroy()
        master_window.focus_set()

    gw.protocol("WM_DELETE_WINDOW", on_closing)

    # Tabbed interface
    notebook = ttk.Notebook(gw)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- Tab 1: Income vs Taxes ---
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Income vs Taxes")
    
    fig1, ax1 = plt.subplots(figsize=(10,6))
    line1, = ax1.plot(incomes, box1_tax, 'b-', label='loonheffing')
    line2, = ax1.plot(incomes, box1_total, 'r-', label='Box1 totaal')
    line3, = ax1.plot(incomes, aanslag, 'y-', label='Aanslag incl heffingen')   

    ax1.set(xlabel='Income (€)', ylabel='Amount (€)', title='Tax Analysis')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(0, color='k', lw=1)
    add_crosshair(fig1, ax1, [line1, line2, line3])
    
    canvas1 = FigureCanvasTkAgg(fig1, tab1)
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    NavigationToolbar2Tk(canvas1, tab1).update()

    # --- Tab 2: Kortingen Analysis ---
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Kortingen Breakdown")
    
    fig2, ax2 = plt.subplots(figsize=(10,6))
    lines_kort = [
        ax2.plot(incomes, heffingskorting, 'b-', label='Heffings Korting')[0],
        ax2.plot(incomes, arbeidskorting, 'g-', label='Arbeids Korting')[0],
        ax2.plot(incomes, ouderenkorting, 'm-', label='Ouderen Korting')[0],
        ax2.plot(incomes, kortingen, 'r-', label='Total Kortingen')[0]
    ]
    
    ax2.set(xlabel='Income (€)', ylabel='Amount (€)', title='Kortingen Analysis')
    ax2.grid(True, alpha=0.3)
    add_crosshair(fig2, ax2, lines_kort)
    
    canvas2 = FigureCanvasTkAgg(fig2, tab2)
    canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    NavigationToolbar2Tk(canvas2, tab2).update()

    # --- Tab 3: Premies Analysis ---
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Premies Analysis")
    
    fig3, ax3 = plt.subplots(figsize=(10,6))
    line_prem, = ax3.plot(incomes, premies, 'b-', label='Premies Volksverz')
    
    ax3.set(xlabel='Income (€)', ylabel='Amount (€)', title='Premies Analysis')
    ax3.grid(True, alpha=0.3)
    add_crosshair(fig3, ax3, [line_prem])
    
    canvas3 = FigureCanvasTkAgg(fig3, tab3)
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    NavigationToolbar2Tk(canvas3, tab3).update()