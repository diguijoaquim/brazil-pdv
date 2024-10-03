from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle

def create_pdf(filename, data):
    # Configurações básicas do documento PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Cor de fundo personalizada (amber)
    amber_light = colors.HexColor('#FFBF00')

    # Dados fictícios dos funcionários
    funcionarios = [
        {"Nome": "João Silva", "Cargo": "Enfermeiro", "Setor": "Emergência"},
        {"Nome": "Maria Souza", "Cargo": "Médica", "Setor": "Clínica Geral"},
        {"Nome": "Carlos Santos", "Cargo": "Técnico de Enfermagem", "Setor": "UTI"},
        {"Nome": "Ana Oliveira", "Cargo": "Administrativo", "Setor": "RH"}
    ]

    # Estilo de tabela com cores personalizadas
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), amber_light),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),  # Cor de fundo das células
    ])

    # Criação da tabela
    data_with_headers = [["Nome", "Cargo", "Setor"]]
    for func in funcionarios:
        data_with_headers.append([func["Nome"], func["Cargo"], func["Setor"]])

    t = Table(data_with_headers)
    t.setStyle(style)

    # Desenha a tabela no PDF
    w, h = t.wrap(width, height)
    t.drawOn(c, 72, height - h - 50)

    # Fecha o PDF
    c.save()

# Exemplo de uso da função
create_pdf("funcionarios_hospital.pdf", [])
