import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from database.db_manager import DatabaseManager

class InventoryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DatabaseManager()
        
        # Create treeview
        self.tree = ttk.Treeview(self, 
            columns=('Date', 'Name', 'PrevStock', 'Entries', 'Outputs', 'Price', 'FinalQty', 'Comment'),
            show='headings',
            style='Modern.Treeview')
        
        # [Configuration du Treeview reste identique...]
        
        # Ajout du bouton Enregistrer
        ttk.Button(buttons_frame, text="Enregistrer", 
                  style='Modern.TButton',
                  command=self.save_inventory).pack(side=tk.LEFT, padx=5)
        
        self.refresh_inventory()

    def save_inventory(self):
        """Sauvegarder l'inventaire dans la base de données"""
        try:
            name = self.name_var.get()
            entries = int(self.entries_var.get() or 0)
            price = float(self.price_var.get() or 0)
            
            if self.db.save_motorcycle(name, entries, price):
                messagebox.showinfo("Succès", "Inventaire sauvegardé!")
                self.refresh_inventory()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la sauvegarde!")
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides!")

    def refresh_inventory(self):
        """Rafraîchir l'affichage de l'inventaire"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for motorcycle in self.db.get_inventory():
            self.tree.insert('', 'end', values=(
                datetime.now().strftime("%Y-%m-%d"),
                motorcycle[0],  # name
                motorcycle[1],  # quantity
                0,  # entries
                0,  # outputs
                f"{motorcycle[2]:.2f}",  # price
                motorcycle[1],  # final quantity
                ""  # comment
            ))