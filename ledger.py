"""
Daily Settlement Ledger - Main Application
Provides a CLI interface for managing settlement ledger entries
"""
import sys
from database import SettlementLedgerDB


def format_currency(value):
    """Format a value as currency, handling None values"""
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def display_entry(entry):
    """Display a single entry in a formatted way"""
    if not entry:
        print("Entry not found.")
        return
    
    entry_id, name, prev_bal, prev_total, seller1, seller2, seller3, seller4, today_total, today_bal, created_at, updated_at = entry
    
    print("\n" + "="*60)
    print(f"Entry ID: {entry_id}")
    print(f"Name: {name}")
    print(f"Created: {created_at}")
    print(f"Last Updated: {updated_at}")
    print("-"*60)
    print("Previous Settlement:")
    print(f"  Previous Balance: {format_currency(prev_bal)}")
    print(f"  Previous Total: {format_currency(prev_total)}")
    print("-"*60)
    print("Seller Amounts:")
    print(f"  Seller 1: {format_currency(seller1)}")
    print(f"  Seller 2: {format_currency(seller2)}")
    print(f"  Seller 3: {format_currency(seller3)}")
    print(f"  Seller 4: {format_currency(seller4)}")
    print("-"*60)
    print("Today's Settlement:")
    print(f"  Today's Total: {format_currency(today_total)}")
    print(f"  Today's Balance: {format_currency(today_bal)}")
    print("="*60 + "\n")


def display_all_entries(entries):
    """Display all entries in a table format"""
    if not entries:
        print("\nNo entries found in the ledger.\n")
        return
    
    print("\n" + "="*100)
    print(f"{'ID':<5} {'Name':<20} {'Prev Bal':<12} {'Prev Total':<12} {'S1':<10} {'S2':<10} {'S3':<10} {'S4':<10} {'Today Total':<12} {'Today Bal':<12}")
    print("-"*100)
    
    for entry in entries:
        entry_id, name, prev_bal, prev_total, seller1, seller2, seller3, seller4, today_total, today_bal, created_at, updated_at = entry
        
        print(f"{entry_id:<5} {name[:18]:<20} {format_currency(prev_bal):<12} {format_currency(prev_total):<12} "
              f"{format_currency(seller1):<10} {format_currency(seller2):<10} {format_currency(seller3):<10} "
              f"{format_currency(seller4):<10} {format_currency(today_total):<12} {format_currency(today_bal):<12}")
    
    print("="*100 + "\n")


def get_float_input(prompt, allow_empty=True):
    """Get a float input from the user, allowing empty/NULL values"""
    while True:
        value = input(prompt).strip()
        if allow_empty and value == "":
            return None
        try:
            return float(value) if value else None
        except ValueError:
            print("Please enter a valid number or leave empty for NULL.")


def add_entry_menu(db):
    """Menu for adding a new entry"""
    print("\n--- Add New Entry ---")
    name = input("Enter name: ").strip()
    if not name:
        print("Name is required!")
        return
    
    print("\nPrevious Settlement (press Enter to leave as NULL):")
    previous_balance = get_float_input("Previous Balance: ")
    previous_total = get_float_input("Previous Total: ")
    
    print("\nSeller Amounts (press Enter to leave as NULL):")
    seller_1 = get_float_input("Seller 1: ")
    seller_2 = get_float_input("Seller 2: ")
    seller_3 = get_float_input("Seller 3: ")
    seller_4 = get_float_input("Seller 4: ")
    
    print("\nToday's Settlement (press Enter to leave as NULL):")
    today_total = get_float_input("Today's Total: ")
    today_balance = get_float_input("Today's Balance: ")
    
    entry_id = db.add_entry(name, previous_balance, previous_total,
                           seller_1, seller_2, seller_3, seller_4,
                           today_total, today_balance)
    print(f"\nEntry added successfully with ID: {entry_id}")


def view_entry_menu(db):
    """Menu for viewing a specific entry"""
    try:
        entry_id = int(input("\nEnter entry ID to view: "))
        entry = db.get_entry(entry_id)
        display_entry(entry)
    except ValueError:
        print("Please enter a valid ID number.")


def update_entry_menu(db):
    """Menu for updating an entry"""
    try:
        entry_id = int(input("\nEnter entry ID to update: "))
        entry = db.get_entry(entry_id)
        if not entry:
            print("Entry not found!")
            return
        
        print("\nCurrent entry:")
        display_entry(entry)
        print("\nEnter new values (press Enter to skip/keep current value):")
        
        name = input("Name: ").strip()
        name = name if name else None
        
        print("\nPrevious Settlement:")
        previous_balance = get_float_input("Previous Balance: ")
        previous_total = get_float_input("Previous Total: ")
        
        print("\nSeller Amounts:")
        seller_1 = get_float_input("Seller 1: ")
        seller_2 = get_float_input("Seller 2: ")
        seller_3 = get_float_input("Seller 3: ")
        seller_4 = get_float_input("Seller 4: ")
        
        print("\nToday's Settlement:")
        today_total = get_float_input("Today's Total: ")
        today_balance = get_float_input("Today's Balance: ")
        
        # Only update fields that were provided
        update_dict = {}
        if name is not None:
            update_dict['name'] = name
        if previous_balance is not None:
            update_dict['previous_balance'] = previous_balance
        if previous_total is not None:
            update_dict['previous_total'] = previous_total
        if seller_1 is not None:
            update_dict['seller_1'] = seller_1
        if seller_2 is not None:
            update_dict['seller_2'] = seller_2
        if seller_3 is not None:
            update_dict['seller_3'] = seller_3
        if seller_4 is not None:
            update_dict['seller_4'] = seller_4
        if today_total is not None:
            update_dict['today_total'] = today_total
        if today_balance is not None:
            update_dict['today_balance'] = today_balance
        
        if db.update_entry(entry_id, **update_dict):
            print("\nEntry updated successfully!")
        else:
            print("\nUpdate failed or no changes were made.")
    except ValueError:
        print("Please enter a valid ID number.")


def delete_entry_menu(db):
    """Menu for deleting an entry"""
    try:
        entry_id = int(input("\nEnter entry ID to delete: "))
        entry = db.get_entry(entry_id)
        if not entry:
            print("Entry not found!")
            return
        
        print("\nEntry to be deleted:")
        display_entry(entry)
        confirm = input("\nAre you sure you want to delete this entry? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            if db.delete_entry(entry_id):
                print("Entry deleted successfully!")
            else:
                print("Delete failed!")
        else:
            print("Delete cancelled.")
    except ValueError:
        print("Please enter a valid ID number.")


def search_entry_menu(db):
    """Menu for searching entries by name"""
    search_term = input("\nEnter name to search for: ").strip()
    if not search_term:
        print("Please enter a search term.")
        return
    
    entries = db.search_by_name(search_term)
    if entries:
        print(f"\nFound {len(entries)} matching entries:")
        display_all_entries(entries)
    else:
        print("\nNo matching entries found.")


def main_menu(db):
    """Display the main menu and handle user choices"""
    while True:
        print("\n" + "="*60)
        print("Daily Settlement Ledger")
        print("="*60)
        print("1. Add New Entry")
        print("2. View All Entries")
        print("3. View Entry by ID")
        print("4. Update Entry")
        print("5. Delete Entry")
        print("6. Search Entries by Name")
        print("7. Exit")
        print("="*60)
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            add_entry_menu(db)
        elif choice == '2':
            entries = db.get_all_entries()
            display_all_entries(entries)
        elif choice == '3':
            view_entry_menu(db)
        elif choice == '4':
            update_entry_menu(db)
        elif choice == '5':
            delete_entry_menu(db)
        elif choice == '6':
            search_entry_menu(db)
        elif choice == '7':
            print("\nThank you for using Daily Settlement Ledger!")
            break
        else:
            print("\nInvalid option. Please select 1-7.")


def main():
    """Main function to start the application"""
    db = SettlementLedgerDB()
    
    try:
        main_menu(db)
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

