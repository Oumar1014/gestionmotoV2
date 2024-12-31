import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from database.db_manager import DatabaseManager
from utils.pdf_generator import PDFGenerator

class ReportsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DatabaseManager()
        
        # [Configuration des filtres reste identique...]
        
        # Modification du Treeview pour édition directe
        self.tree = ttk.Treeview(self, 
            columns=('Date', 'Motorcycle', 'Client', 'Quantity', 'Price', 'Total'),
            show='headings',
            style='Modern.Treeview')
        
        # Configuration des colonnes éditables
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # [Reste de la configuration...]

    def on_double_click(self, event):
        """Gérer l'édition directe dans le tableau"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            # Créer un widget d'édition
            self.edit_cell(item, column)

    def edit_cell(self, item, column):
        """Créer un widget d'édition pour la cellule"""
        # Demander le code d'accès
        dialog = tk.Toplevel(self)
        dialog.title("Code d'accès")
        
        ttk.Label(dialog, text="Entrez le code d'accès:").pack(pady=10)
        code_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=code_var, show="*").pack(pady=5)
        
        def verify_code():
            if code_var.get() == "Bamma1234":
                dialog.destroy()
                self.show_edit_widget(item, column)
            else:
                messagebox.showerror("Erreur", "Code d'accès incorrect!")
                dialog.destroy()
        
        ttk.Button(dialog, text="Valider", command=verify_code).pack(pady=10)

    def show_edit_widget(self, item, column):
        """Afficher le widget d'édition"""
        x, y, w, h = self.tree.bbox(item, column)
        
        # Créer l'entry widget
        entry = ttk.Entry(self.tree, width=20)
        entry.place(x=x, y=y, width=w, height=h)
        
        # Récupérer la valeur actuelle
        current_value = self.tree.set(item, column)
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.focus()
        
        def save_edit(event=None):
            """Sauvegarder la modification"""
            new_value = entry.get()
            sale_id = self.tree.item(item)['values'][0]  # Assuming first column is ID
            
            # Update in database
            if self.db.update_sale(sale_id, new_value):
                self.tree.set(item, column, new_value)
                entry.destroy()
                self.refresh_report()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la mise à jour!")
                entry.destroy()
        
        entry.bind('<Return>', save_edit)
        entry.bind('<Escape>', lambda e: entry.destroy())

    def print_report(self):
        """Générer le rapport PDF"""
        try:
            selected_date = self.date_filter.get_date()
            sales_data = self.db.get_sales_report(selected_date)
            
            filename = PDFGenerator.generate_sales_report(selected_date, sales_data)
            messagebox.showinfo("Succès", f"Rapport généré: {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport: {str(e)}")