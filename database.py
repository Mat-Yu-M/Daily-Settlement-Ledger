"""
Database module for Daily Settlement Ledger
Handles all SQLite database operations
"""
import sqlite3
from typing import Optional, List, Tuple
from datetime import datetime


class SettlementLedgerDB:
    """Database handler for the Daily Settlement Ledger"""
    
    def __init__(self, db_path: str = "settlement_ledger.db"):
        """
        Initialize the database connection
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database and create the table if it doesn't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create the settlement_ledger table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settlement_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                previous_balance REAL,
                previous_total REAL,
                seller_1 REAL,
                seller_2 REAL,
                seller_3 REAL,
                seller_4 REAL,
                today_total REAL,
                today_balance REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def add_entry(self, name: str, previous_balance: Optional[float] = None,
                  previous_total: Optional[float] = None,
                  seller_1: Optional[float] = None,
                  seller_2: Optional[float] = None,
                  seller_3: Optional[float] = None,
                  seller_4: Optional[float] = None,
                  today_total: Optional[float] = None,
                  today_balance: Optional[float] = None) -> int:
        """
        Add a new entry to the ledger
        
        Args:
            name: Name of the entry
            previous_balance: Previous balance (nullable)
            previous_total: Previous total (nullable)
            seller_1: Seller 1 amount (nullable)
            seller_2: Seller 2 amount (nullable)
            seller_3: Seller 3 amount (nullable)
            seller_4: Seller 4 amount (nullable)
            today_total: Today's total (nullable)
            today_balance: Today's balance (nullable)
        
        Returns:
            The ID of the inserted entry
        """
        self.cursor.execute("""
            INSERT INTO settlement_ledger 
            (name, previous_balance, previous_total, seller_1, seller_2, 
             seller_3, seller_4, today_total, today_balance, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (name, previous_balance, previous_total, seller_1, seller_2,
              seller_3, seller_4, today_total, today_balance))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_entry(self, entry_id: int) -> Optional[Tuple]:
        """
        Get a single entry by ID
        
        Args:
            entry_id: The ID of the entry
        
        Returns:
            A tuple containing the entry data, or None if not found
        """
        self.cursor.execute("""
            SELECT id, name, previous_balance, previous_total, seller_1, seller_2,
                   seller_3, seller_4, today_total, today_balance, created_at, updated_at
            FROM settlement_ledger
            WHERE id = ?
        """, (entry_id,))
        return self.cursor.fetchone()
    
    def get_all_entries(self) -> List[Tuple]:
        """
        Get all entries from the ledger
        
        Returns:
            A list of tuples containing all entries
        """
        self.cursor.execute("""
            SELECT id, name, previous_balance, previous_total, seller_1, seller_2,
                   seller_3, seller_4, today_total, today_balance, created_at, updated_at
            FROM settlement_ledger
            ORDER BY updated_at DESC
        """)
        return self.cursor.fetchall()
    
    def update_entry(self, entry_id: int, name: Optional[str] = None,
                     previous_balance: Optional[float] = None,
                     previous_total: Optional[float] = None,
                     seller_1: Optional[float] = None,
                     seller_2: Optional[float] = None,
                     seller_3: Optional[float] = None,
                     seller_4: Optional[float] = None,
                     today_total: Optional[float] = None,
                     today_balance: Optional[float] = None) -> bool:
        """
        Update an existing entry
        
        Args:
            entry_id: The ID of the entry to update
            name: Name of the entry (optional)
            previous_balance: Previous balance (optional)
            previous_total: Previous total (optional)
            seller_1: Seller 1 amount (optional)
            seller_2: Seller 2 amount (optional)
            seller_3: Seller 3 amount (optional)
            seller_4: Seller 4 amount (optional)
            today_total: Today's total (optional)
            today_balance: Today's balance (optional)
        
        Returns:
            True if update was successful, False otherwise
        """
        # Build dynamic update query based on provided fields
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if previous_balance is not None:
            updates.append("previous_balance = ?")
            params.append(previous_balance)
        if previous_total is not None:
            updates.append("previous_total = ?")
            params.append(previous_total)
        if seller_1 is not None:
            updates.append("seller_1 = ?")
            params.append(seller_1)
        if seller_2 is not None:
            updates.append("seller_2 = ?")
            params.append(seller_2)
        if seller_3 is not None:
            updates.append("seller_3 = ?")
            params.append(seller_3)
        if seller_4 is not None:
            updates.append("seller_4 = ?")
            params.append(seller_4)
        if today_total is not None:
            updates.append("today_total = ?")
            params.append(today_total)
        if today_balance is not None:
            updates.append("today_balance = ?")
            params.append(today_balance)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(entry_id)
        
        query = f"UPDATE settlement_ledger SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def update_entry_complete(self, entry_id: int, name: str,
                             previous_balance: Optional[float],
                             previous_total: Optional[float],
                             seller_1: Optional[float],
                             seller_2: Optional[float],
                             seller_3: Optional[float],
                             seller_4: Optional[float],
                             today_total: Optional[float],
                             today_balance: Optional[float]) -> bool:
        """
        Update all fields of an entry (including setting to NULL)
        This method updates all fields, allowing None values to clear fields.
        
        Args:
            entry_id: The ID of the entry to update
            name: Name of the entry (required)
            previous_balance: Previous balance (None to clear)
            previous_total: Previous total (None to clear)
            seller_1: Seller 1 amount (None to clear)
            seller_2: Seller 2 amount (None to clear)
            seller_3: Seller 3 amount (None to clear)
            seller_4: Seller 4 amount (None to clear)
            today_total: Today's total (None to clear)
            today_balance: Today's balance (None to clear)
        
        Returns:
            True if update was successful, False otherwise
        """
        self.cursor.execute("""
            UPDATE settlement_ledger 
            SET name = ?, 
                previous_balance = ?,
                previous_total = ?,
                seller_1 = ?,
                seller_2 = ?,
                seller_3 = ?,
                seller_4 = ?,
                today_total = ?,
                today_balance = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, previous_balance, previous_total, seller_1, seller_2,
              seller_3, seller_4, today_total, today_balance, entry_id))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete an entry from the ledger
        
        Args:
            entry_id: The ID of the entry to delete
        
        Returns:
            True if deletion was successful, False otherwise
        """
        self.cursor.execute("DELETE FROM settlement_ledger WHERE id = ?", (entry_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def search_by_name(self, name: str) -> List[Tuple]:
        """
        Search for entries by name (case-insensitive partial match)
        
        Args:
            name: The name to search for
        
        Returns:
            A list of tuples containing matching entries
        """
        self.cursor.execute("""
            SELECT id, name, previous_balance, previous_total, seller_1, seller_2,
                   seller_3, seller_4, today_total, today_balance, created_at, updated_at
            FROM settlement_ledger
            WHERE name LIKE ?
            ORDER BY updated_at DESC
        """, (f"%{name}%",))
        return self.cursor.fetchall()
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

