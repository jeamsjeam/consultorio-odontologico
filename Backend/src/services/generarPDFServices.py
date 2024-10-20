from ..models.paciente import Paciente
from fpdf import FPDF
import pdb

class GenerarPDF(FPDF):
    def __init__(self, logo_path, titulo):
        super().__init__()
        self.logo_path = logo_path
        self.titulo = titulo

    
    def footer(self):
        # Posición en pie de página
        self.set_y(-15)
        # Número de página
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')
