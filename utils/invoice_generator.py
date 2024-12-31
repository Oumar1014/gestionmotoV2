from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

class InvoiceGenerator:
    @staticmethod
    def generate_invoice(sale_data: dict) -> str:
        filename = f"facture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # En-tête de la société
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, "NOUHOU BAMMA TOURE")
        c.setFont("Helvetica", 10)
        c.drawString(50, 785, "Vendeur des motos")
        c.drawString(50, 770, "Tel : (+223) 77873789 / 90434307 / 83211674")
        c.drawString(50, 755, "Adresse : 5eme Quartier GAO Rep.Du Mali")
        c.drawString(50, 740, "SANILI - KTM")
        c.drawString(50, 725, "NIF : 071003788R - RCCM : Ma.Gao.2013.A.36")
        
        # Numéro et date de facture
        c.setFont("Helvetica-Bold", 16)
        c.drawString(400, 800, "FACTURE")
        c.setFont("Helvetica", 12)
        c.drawString(400, 780, f"N° {datetime.now().strftime('%Y%m%d%H%M')}")
        c.drawString(400, 765, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        
        # Informations client
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 680, "CLIENT")
        c.setFont("Helvetica", 10)
        c.drawString(50, 665, f"Nom: {sale_data['client_name']}")
        c.drawString(50, 650, f"Adresse: {sale_data['client_address']}")
        c.drawString(50, 635, f"Téléphone: {sale_data['client_phone']}")
        
        # Tableau des produits
        y = 580
        # En-têtes du tableau
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "DESCRIPTION")
        c.drawString(250, y, "PRIX UNITAIRE")
        c.drawString(350, y, "QUANTITÉ")
        c.drawString(450, y, "TOTAL")
        
        # Ligne de séparation
        y -= 15
        c.line(50, y, 550, y)
        
        # Données du produit
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, sale_data['name'])
        c.drawString(250, y, f"{sale_data['price']:,.0f} FCFA")
        c.drawString(350, y, str(sale_data['quantity']))
        c.drawString(450, y, f"{sale_data['quantity'] * sale_data['price']:,.0f} FCFA")
        
        # Total
        y -= 40
        c.line(50, y+10, 550, y+10)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, y, "TOTAL:")
        c.drawString(450, y, f"{sale_data['quantity'] * sale_data['price']:,.0f} FCFA")
        
        # Pied de page
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 50, "Merci de votre confiance")
        
        c.save()
        return filename