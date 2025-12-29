"""

V1.0.0
Daily Settlement Ledger - GUI Application
Provides a graphical user interface for managing settlement ledger entries

"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import SettlementLedgerDB
from typing import Optional
from datetime import datetime
import pytz


class EntryDialog:
    """Dialog window for adding/editing entries"""
    
    def __init__(self, parent, title: str, entry_data: Optional[dict] = None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        # Variables
        self.name_var = tk.StringVar(value=entry_data.get('name', '') if entry_data else '')
        self.prev_balance_var = tk.StringVar(value=str(entry_data.get('previous_balance', '')) if entry_data and entry_data.get('previous_balance') is not None else '')
        self.prev_total_var = tk.StringVar(value=str(entry_data.get('previous_total', '')) if entry_data and entry_data.get('previous_total') is not None else '')
        self.seller1_var = tk.StringVar(value=str(entry_data.get('seller_1', '')) if entry_data and entry_data.get('seller_1') is not None else '')
        self.seller2_var = tk.StringVar(value=str(entry_data.get('seller_2', '')) if entry_data and entry_data.get('seller_2') is not None else '')
        self.seller3_var = tk.StringVar(value=str(entry_data.get('seller_3', '')) if entry_data and entry_data.get('seller_3') is not None else '')
        self.seller4_var = tk.StringVar(value=str(entry_data.get('seller_4', '')) if entry_data and entry_data.get('seller_4') is not None else '')
        self.today_total_var = tk.StringVar(value=str(entry_data.get('today_total', '')) if entry_data and entry_data.get('today_total') is not None else '')
        self.today_balance_var = tk.StringVar(value=str(entry_data.get('today_balance', '')) if entry_data and entry_data.get('today_balance') is not None else '')
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name field (required)
        ttk.Label(main_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Previous Settlement section
        prev_frame = ttk.LabelFrame(main_frame, text="Previous Settlement", padding="5")
        prev_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(prev_frame, text="Previous Balance:").grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(prev_frame, textvariable=self.prev_balance_var, width=30).grid(row=0, column=1, sticky=tk.EW, pady=3, padx=5)
        
        ttk.Label(prev_frame, text="Previous Total:").grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(prev_frame, textvariable=self.prev_total_var, width=30).grid(row=1, column=1, sticky=tk.EW, pady=3, padx=5)
        
        prev_frame.columnconfigure(1, weight=1)
        
        # Seller Amounts section
        seller_frame = ttk.LabelFrame(main_frame, text="Seller Amounts", padding="5")
        seller_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        sellers = [
            ("Seller 1:", self.seller1_var),
            ("Seller 2:", self.seller2_var),
            ("Seller 3:", self.seller3_var),
            ("Seller 4:", self.seller4_var),
        ]
        
        for i, (label, var) in enumerate(sellers):
            ttk.Label(seller_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=3)
            ttk.Entry(seller_frame, textvariable=var, width=30).grid(row=i, column=1, sticky=tk.EW, pady=3, padx=5)
        
        seller_frame.columnconfigure(1, weight=1)
        
        # Today's Settlement section
        today_frame = ttk.LabelFrame(main_frame, text="Today's Settlement", padding="5")
        today_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(today_frame, text="Today's Total:").grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(today_frame, textvariable=self.today_total_var, width=30).grid(row=0, column=1, sticky=tk.EW, pady=3, padx=5)
        
        ttk.Label(today_frame, text="Today's Balance:").grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(today_frame, textvariable=self.today_balance_var, width=30).grid(row=1, column=1, sticky=tk.EW, pady=3, padx=5)
        
        today_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
        name_entry.focus()
    
    def _parse_float(self, value: str) -> Optional[float]:
        """Parse a string to float, returning None if empty"""
        value = value.strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None
    
    def _save(self):
        """Save the entry data"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        self.result = {
            'name': name,
            'previous_balance': self._parse_float(self.prev_balance_var.get()),
            'previous_total': self._parse_float(self.prev_total_var.get()),
            'seller_1': self._parse_float(self.seller1_var.get()),
            'seller_2': self._parse_float(self.seller2_var.get()),
            'seller_3': self._parse_float(self.seller3_var.get()),
            'seller_4': self._parse_float(self.seller4_var.get()),
            'today_total': self._parse_float(self.today_total_var.get()),
            'today_balance': self._parse_float(self.today_balance_var.get()),
        }
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result


class SettlementLedgerGUI:
    """Main GUI application for Daily Settlement Ledger"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Settlement Ledger")
        self.root.geometry("1200x700")
        
        # Database connection
        self.db = SettlementLedgerDB()
        
        # Inline editing variables
        self.editing_entry = None
        self.editing_item = None
        self.editing_column = None
        self.tree_frame = None  # Will be set in _create_widgets
        
        # Column to database field mapping (excluding ID and PH Date columns)
        self.column_to_field = {
            'Name': 'name',
            'Prev Balance': 'previous_balance',
            'Prev Total': 'previous_total',
            'Seller 1': 'seller_1',
            'Seller 2': 'seller_2',
            'Seller 3': 'seller_3',
            'Seller 4': 'seller_4',
            'Today Total': 'today_total',
            'Today Balance': 'today_balance',
        }
        self.non_editable_columns = {'ID', 'Date (PH time)'}
        
        # Currency columns (need parsing)
        self.currency_columns = {'Prev Balance', 'Prev Total', 'Seller 1', 'Seller 2', 
                                'Seller 3', 'Seller 4', 'Today Total', 'Today Balance'}
        
        # Create UI
        self._create_widgets()
        self._refresh_table()
        
        # Center window
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Top toolbar
        toolbar = ttk.Frame(self.root, padding="10")
        toolbar.pack(fill=tk.X)
        
        ttk.Button(toolbar, text="Add New Entry", command=self._add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Entry", command=self._edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Entry", command=self._delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_table).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._search_entries())
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Treeview with scrollbars
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree_frame = tree_frame  # Store reference for inline editing
        
        # Define columns
        columns = ('ID', 'Date (PH time)', 'Name', 'Prev Balance', 'Prev Total', 'Seller 1', 'Seller 2', 
                  'Seller 3', 'Seller 4', 'Today Total', 'Today Balance')
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Configure column headings and widths
        column_configs = [
            ('ID', 50),
            ('Date (PH time)', 140),
            ('Name', 140),
            ('Prev Balance', 100),
            ('Prev Total', 100),
            ('Seller 1', 90),
            ('Seller 2', 90),
            ('Seller 3', 90),
            ('Seller 4', 90),
            ('Today Total', 100),
            ('Today Balance', 100),
        ]
        
        for col, width in column_configs:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to inline edit
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        
        # Bind Enter key to edit (only if not inline editing)
        self.root.bind('<Return>', lambda e: self._handle_return_key())
        self.root.bind('<Delete>', lambda e: self._delete_entry())
        self.root.bind('<Escape>', lambda e: self._cancel_inline_edit())
    
    def _format_currency(self, value):
        """Format a value as currency"""
        if value is None:
            return ""
        return f"${float(value):,.2f}"
    
    def _parse_currency(self, value_str):
        """Parse a currency string to float, returns None if empty/invalid"""
        if not value_str or value_str.strip() == "":
            return None
        try:
            # Remove $, commas, and whitespace
            cleaned = value_str.strip().replace('$', '').replace(',', '').strip()
            if cleaned == "":
                return None
            return float(cleaned)
        except (ValueError, AttributeError):
            return None
    
    def _convert_to_ph_time(self, utc_str):
        """Convert UTC timestamp string to Asia/Manila formatted string"""
        if not utc_str:
            return "N/A"
        try:
            # Try common sqlite formats
            try:
                dt_utc = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt_utc = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S.%f")
            utc = pytz.timezone('UTC')
            manila = pytz.timezone('Asia/Manila')
            dt_utc = utc.localize(dt_utc)
            dt_ph = dt_utc.astimezone(manila)
            return dt_ph.strftime("%Y-%m-%d %I:%M:%S %p")
        except Exception:
            return utc_str or 'N/A'

    def _refresh_table(self):
        """Refresh the table with all entries"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all entries
        entries = self.db.get_all_entries()
        
        # Insert entries
        for entry in entries:
            entry_id, name, prev_bal, prev_total, seller1, seller2, seller3, seller4, today_total, today_bal, created_at, updated_at = entry
            ph_date_str = self._convert_to_ph_time(created_at)
            values = (
                entry_id,
                ph_date_str,
                name,
                self._format_currency(prev_bal),
                self._format_currency(prev_total),
                self._format_currency(seller1),
                self._format_currency(seller2),
                self._format_currency(seller3),
                self._format_currency(seller4),
                self._format_currency(today_total),
                self._format_currency(today_bal),
            )
            self.tree.insert('', tk.END, values=values)
        
        self.status_var.set(f"Total entries: {len(entries)}")
    
    def _search_entries(self):
        """Search entries by name"""
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            entries = self.db.search_by_name(search_term)
        else:
            entries = self.db.get_all_entries()
        
        # Insert matching entries
        for entry in entries:
            entry_id, name, prev_bal, prev_total, seller1, seller2, seller3, seller4, today_total, today_bal, created_at, updated_at = entry
            ph_date_str = self._convert_to_ph_time(created_at)
            values = (
                entry_id,
                ph_date_str,
                name,
                self._format_currency(prev_bal),
                self._format_currency(prev_total),
                self._format_currency(seller1),
                self._format_currency(seller2),
                self._format_currency(seller3),
                self._format_currency(seller4),
                self._format_currency(today_total),
                self._format_currency(today_bal),
            )
            self.tree.insert('', tk.END, values=values)
        
        self.status_var.set(f"Found {len(entries)} entries")
    
    def _get_selected_entry_id(self):
        """Get the ID of the selected entry"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        return item['values'][0]  # First column is ID
    
    def _add_entry(self):
        """Add a new entry"""
        dialog = EntryDialog(self.root, "Add New Entry")
        result = dialog.show()
        
        if result:
            try:
                self.db.add_entry(**result)
                self._refresh_table()
                self.status_var.set("Entry added successfully")
                messagebox.showinfo("Success", "Entry added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add entry: {str(e)}")
    
    def _edit_entry(self):
        """Edit the selected entry"""
        entry_id = self._get_selected_entry_id()
        if not entry_id:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return
        
        # Get current entry data
        entry = self.db.get_entry(entry_id)
        if not entry:
            messagebox.showerror("Error", "Entry not found!")
            return
        
        # Prepare entry data for dialog
        entry_data = {
            'name': entry[1],
            'previous_balance': entry[2],
            'previous_total': entry[3],
            'seller_1': entry[4],
            'seller_2': entry[5],
            'seller_3': entry[6],
            'seller_4': entry[7],
            'today_total': entry[8],
            'today_balance': entry[9],
        }
        
        dialog = EntryDialog(self.root, f"Edit Entry #{entry_id}", entry_data)
        result = dialog.show()
        
        if result:
            try:
                # Update all fields (including None values to clear fields)
                self.db.update_entry_complete(
                    entry_id,
                    result['name'],
                    result['previous_balance'],
                    result['previous_total'],
                    result['seller_1'],
                    result['seller_2'],
                    result['seller_3'],
                    result['seller_4'],
                    result['today_total'],
                    result['today_balance']
                )
                self._refresh_table()
                self.status_var.set("Entry updated successfully")
                messagebox.showinfo("Success", "Entry updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update entry: {str(e)}")
    
    def _delete_entry(self):
        """Delete the selected entry"""
        # Cancel any ongoing inline edit
        if self.editing_entry:
            self._cancel_inline_edit()
        
        entry_id = self._get_selected_entry_id()
        if not entry_id:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return
        
        # Get entry name for confirmation
        entry = self.db.get_entry(entry_id)
        if not entry:
            messagebox.showerror("Error", "Entry not found!")
            return
        
        entry_name = entry[1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete entry '{entry_name}' (ID: {entry_id})?"):
            try:
                self.db.delete_entry(entry_id)
                self._refresh_table()
                self.status_var.set("Entry deleted successfully")
                messagebox.showinfo("Success", "Entry deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def _on_tree_double_click(self, event):
        """Handle double-click on treeview to start inline editing"""
        # Cancel any existing inline edit
        if self.editing_entry:
            self._cancel_inline_edit()
        
        # Identify the region clicked
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        # Get the item and column
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if not item or not column:
            return
        
        # Convert column number (e.g., '#1', '#2') to index
        column_index = int(column.replace('#', '')) - 1  # Subtract 1 because '#1' is the tree column
        
        # Get column name
        columns = ('ID', 'Date (PH time)', 'Name', 'Prev Balance', 'Prev Total', 'Seller 1', 'Seller 2', 
                  'Seller 3', 'Seller 4', 'Today Total', 'Today Balance')
        
        if column_index < 0 or column_index >= len(columns):
            return
        
        column_name = columns[column_index]
        
        # Don't allow editing ID or PH Date column
        if column_name in self.non_editable_columns:
            # Open edit dialog for ID, do nothing for date
            if column_name == 'ID':
                self._edit_entry()
            return
        
        # Start inline editing
        self._start_inline_edit(item, column_name, column_index)
    
    def _start_inline_edit(self, item, column_name, column_index):
        """Start inline editing for a specific cell"""
        # Get the current value
        item_values = self.tree.item(item, 'values')
        if column_index >= len(item_values):
            return
        
        current_value = item_values[column_index]
        
        # Get the bounding box of the cell (coordinates are relative to treeview)
        bbox = self.tree.bbox(item, column=f"#{column_index + 1}")
        if not bbox:
            return
        
        tree_x, tree_y, width, height = bbox
        
        # Convert coordinates from treeview to tree_frame
        # Get the treeview's position relative to its parent
        tree_frame_x = self.tree.winfo_x()
        tree_frame_y = self.tree.winfo_y()
        
        x = tree_frame_x + tree_x
        y = tree_frame_y + tree_y
        
        # Create entry widget
        entry = ttk.Entry(self.tree_frame)
        
        # For currency columns, remove formatting for editing
        if column_name in self.currency_columns:
            # Parse and show raw number
            parsed = self._parse_currency(current_value)
            entry_value = str(parsed) if parsed is not None else ""
        else:
            entry_value = current_value if current_value else ""
        
        entry.insert(0, entry_value)
        entry.select_range(0, tk.END)
        
        # Place the entry over the cell
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()
        
        # Store editing state
        self.editing_entry = entry
        self.editing_item = item
        self.editing_column = column_name
        self.editing_column_index = column_index
        
        # Bind events
        entry.bind('<Return>', lambda e: self._finish_inline_edit())
        entry.bind('<Escape>', lambda e: self._cancel_inline_edit())
        # Use after_idle to delay FocusOut handling, allowing click events to register first
        entry.bind('<FocusOut>', lambda e: self.root.after_idle(self._check_focus_out))
    
    def _finish_inline_edit(self):
        """Finish inline editing and save the value"""
        if not self.editing_entry:
            return
        
        # Save editing state before cleanup
        entry_widget = self.editing_entry
        editing_item = self.editing_item
        editing_column = self.editing_column
        editing_column_index = self.editing_column_index
        
        # Get the new value before destroying widget
        try:
            new_value = entry_widget.get().strip()
        except tk.TclError:
            self._cancel_inline_edit()
            return  # Widget was already destroyed
        
        # Clean up the editing widget
        self._cancel_inline_edit()
        
        # Get the entry ID
        item_values = self.tree.item(editing_item, 'values')
        entry_id = item_values[0]  # ID is first column
        
        # Get the database field name
        field_name = self.column_to_field.get(editing_column)
        if not field_name:
            return
        
        # Parse the value based on column type
        if editing_column in self.currency_columns:
            # Parse currency value
            parsed_value = self._parse_currency(new_value)
            # Allow None for currency fields
            update_value = parsed_value
        else:
            # For name, use string value (required field)
            if not new_value:
                messagebox.showerror("Error", f"{editing_column} cannot be empty!")
                # Restart editing if validation failed
                self._start_inline_edit(editing_item, editing_column, editing_column_index)
                return
            update_value = new_value
        
        # Update the database
        try:
            # Create update dictionary with only the changed field
            update_dict = {field_name: update_value}
            self.db.update_entry(entry_id, **update_dict)
            
            # Refresh the table to show updated value
            self._refresh_table()
            self.status_var.set(f"{editing_column} updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update {editing_column}: {str(e)}")
            # Restart editing if update failed
            try:
                self._start_inline_edit(editing_item, editing_column, editing_column_index)
            except:
                pass
    
    def _check_focus_out(self):
        """Check if we should finish editing after focus out"""
        # Only finish if entry still exists and doesn't have focus
        if self.editing_entry:
            try:
                # Check if widget still exists and doesn't have focus
                if not self.editing_entry.focus_get() == self.editing_entry:
                    self._finish_inline_edit()
            except tk.TclError:
                # Widget was destroyed, clean up
                self.editing_entry = None
    
    def _cancel_inline_edit(self):
        """Cancel inline editing without saving"""
        if self.editing_entry:
            try:
                self.editing_entry.destroy()
            except tk.TclError:
                pass  # Widget already destroyed
            self.editing_entry = None
            self.editing_item = None
            self.editing_column = None
            if hasattr(self, 'editing_column_index'):
                delattr(self, 'editing_column_index')
    
    def _handle_return_key(self):
        """Handle Return key press - only edit if not inline editing"""
        if not self.editing_entry:
            self._edit_entry()
    
    def on_closing(self):
        """Handle window closing"""
        self.db.close()
        self.root.destroy()


def main():
    """Main function to start the GUI application"""
    root = tk.Tk()
    app = SettlementLedgerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

