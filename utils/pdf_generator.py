from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime

class PDFGenerator:
    @staticmethod
    def generate_sales_report(date: datetime, sales_data: list) -> str:
        filename = f"rapport_ventes_{date.strftime('%Y%m%d')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # En-tête
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, 28*cm, "NOUHOU BAMMA TOURE")
        c.setFont("Helvetica", 10)
        c.drawString(2*cm, 27.5*cm, "Vendeur des motos")
        c.drawString(2*cm, 27*cm, "Tel : (+223) 77873789 / 90434307 / 83211674")
        c.drawString(2*cm, 26.5*cm, "RAPPORT DES VENTES")
        c.drawString(2*cm, 26*cm, f"Date: {date.strftime('%d/%m/%Y')}")
        
        # Tableau
        def draw_table_header():
            headers = ['Date', 'Moto', 'Client', 'Quantité', 'Prix', 'Total']
            x_positions = [2*cm, 5*cm, 8*cm, 12*cm, 15*cm, 18*cm]
            y = 24*cm
            
            # Fond gris pour l'en-tête
            c.setFillColor(colors.lightgrey)
            c.rect(2*cm, y-0.5*cm, 17*cm, 0.8*cm, fill=True)
            c.setFillColor(colors.black)
            
            # Texte de l'en-tête
            c.setFont("Helvetica-Bold", 10)
            for header, x in zip(headers, x_positions):
                c.drawString(x, y, header)
            
            return y - 1*cm
        
        # Dessiner les lignes du tableau
        def draw_table_lines(y_start, y_end):
            c.setStrokeColor(colors.grey)
            c.setLineWidth(0.5)
            # Lignes verticales
            x_positions = [2*cm, 5*cm, 8*cm, 12*cm, 15*cm, 18*cm]
            for x in x_positions:
                c.line(x, y_start+0.8*cm, x, y_end)
            # Ligne horizontale du bas
            c.line(2*cm, y_end, 19*cm, y_end)
        
        y = draw_table_header()
        start_y = y + 1*cm
        
        # Contenu du tableau
        c.setFont("Helvetica", 9)
        total = 0
        
        for sale in sales_data:
            if y < 3*cm:  # Nouvelle page
                draw_table_lines(start_y, y)
                c.showPage()
                y = draw_table_header()
                start_y = y + 1*cm
            
            x_positions = [2*cm, 5*cm, 8*cm, 12*cm, 15*cm, 18*cm]
            c.drawString(x_positions[0], y, sale[1])  # Date
            c.drawString(x_positions[1], y, sale[2])  # Moto
            c.drawString(x_positions[2], y, sale[3])  # Client
            c.drawString(x_positions[3], y, str(sale[4]))  # Quantité
            c.drawString(x_positions[4], y, f"{sale[5]:,.0f}")  # Prix
            c.drawString(x_positions[5], y, f"{sale[6]:,.0f}")  # Total
            
            total += sale[6]
            y -= 0.6*cm
        
        # Lignes du tableau
        draw_table_lines(start_y, y)
        
        # Total
        y -= 1*cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(15*cm, y, "Total:")
        c.drawString(18*cm, y, f"{total:,.0f} FCFA")
        
        c.save()
        return filename