from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import psycopg2
import psycopg2.extras
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
from datetime import datetime
import io
import os
import re

app = Flask(__name__)
CORS(app)

# Configurações do banco - usa variável de ambiente ou local
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # psycopg2 aceita postgresql:// ou postgres://
    DB_CONFIG = DATABASE_URL
else:
    # Configuração local
    DB_CONFIG = {
        'host': '127.0.0.1',
        'database': 'hospitalmp',
        'user': 'postgres',
        'password': '653886',
        'port': '5432'
    }

def get_db_connection():
    """Cria conexão com o banco de dados"""
    if isinstance(DB_CONFIG, str):
        # DATABASE_URL como string
        return psycopg2.connect(DB_CONFIG)
    else:
        # Configuração local como dicionário
        return psycopg2.connect(**DB_CONFIG)

@app.route('/api/tabelas', methods=['GET'])
def listar_tabelas():
    """Retorna lista de todas as tabelas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tabelas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'tabelas': tabelas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buscar', methods=['POST'])
def buscar():
    """Busca termo em todas as tabelas"""
    try:
        data = request.json
        termo = data.get('termo', '').strip()
        
        if not termo:
            return jsonify({'success': False, 'error': 'Termo de busca não informado'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obter lista de tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        tabelas = [row[0] for row in cursor.fetchall()]
        
        resultados = []
        
        for tabela in tabelas:
            try:
                # Obter colunas da tabela
                cursor.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{tabela}'
                """)
                colunas = cursor.fetchall()
                
                # Criar query de busca em colunas de texto
                colunas_texto = [col[0] for col in colunas if 'char' in col[1] or 'text' in col[1]]
                
                if colunas_texto:
                    # Montar condição WHERE
                    condicoes = [f"CAST({col} AS TEXT) ILIKE %s" for col in colunas_texto]
                    where_clause = " OR ".join(condicoes)
                    
                    query = f"SELECT * FROM {tabela} WHERE {where_clause} LIMIT 100"
                    
                    # Executar busca
                    cursor.execute(query, [f'%{termo}%'] * len(colunas_texto))
                    rows = cursor.fetchall()
                    
                    if rows:
                        # Obter nomes das colunas
                        col_names = [desc[0] for desc in cursor.description]
                        
                        # Converter para dicionários
                        registros = []
                        for row in rows:
                            registro = {}
                            for i, val in enumerate(row):
                                registro[col_names[i]] = str(val) if val is not None else None
                            registros.append(registro)
                        
                        resultados.append({
                            'tabela': tabela,
                            'total': len(registros),
                            'registros': registros
                        })
            except:
                pass
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'termo': termo,
            'total_tabelas': len(resultados),
            'resultados': resultados
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tabela/<nome>', methods=['GET'])
def ver_tabela(nome):
    """Retorna dados de uma tabela específica"""
    try:
        limite = request.args.get('limite', 50, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM {nome} LIMIT {limite}"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Obter nomes das colunas
        col_names = [desc[0] for desc in cursor.description]
        
        # Converter para dicionários
        registros = []
        for row in rows:
            registro = {}
            for i, val in enumerate(row):
                registro[col_names[i]] = str(val) if val is not None else None
            registros.append(registro)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'tabela': nome,
            'total': len(registros),
            'colunas': col_names,
            'registros': registros
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/colunas-prescricao')
def colunas_prescricao():
    """Retorna colunas da tabela prescricao"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'prescricao';")
        colunas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'colunas': colunas})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/colunas-exames')
def colunas_exames():
    """Retorna colunas da tabela examescomplementares"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'examescomplementares';")
        colunas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'colunas': colunas})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/', methods=['GET'])
def index():
    """Página inicial da API"""
    return jsonify({
        'status': 'online',
        'message': 'API Hospital BAM está funcionando!',
        'endpoints': {
            'health': '/api/health',
            'buscar_paciente': '/api/buscar-paciente-bam (POST)',
            'gerar_pdf': '/api/gerar-pdf-bam/<id> (GET)',
            'tabelas': '/api/tabelas (GET)'
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica se a API está funcionando"""
    return jsonify({'status': 'ok', 'message': 'API Hospital MP está funcionando!'})

@app.route('/api/buscar-paciente-bam', methods=['POST'])
def buscar_paciente_bam():
    """Busca paciente na tabela BAM pelo nome"""
    try:
        data = request.json
        nome = data.get('nome', '').strip()
        
        if not nome:
            return jsonify({'success': False, 'error': 'Nome do paciente não informado'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Buscar na tabela BAM com JOIN nas tabelas relacionadas
        query = """
SELECT 
    b.idbam,
    b.controle,
    b.data,
    b.hora,
    b.datadaalta,
    b.unidade,
    b.natendente,
    b.receita,
    b.comentariotranferencia,
    b.transferido,
    b.daralta,
    b.ematendimento,
    b.internar,
    b.prioridade,
    p.nome as paciente_nome,
    p.cpf as paciente_cpf,
    p.nascimento as paciente_nascimento,
    p.sexo as paciente_sexo,
    p.telefone as paciente_telefone,
    p.endereco as paciente_endereco,
    p.bairro as paciente_bairro,
    p.municipio as paciente_municipio,
    p.mae as paciente_mae,
    string_agg(pr.prescricao, '\n') as prescricao,
    a.anamnese as avaliacao_anamnese,
    CASE 
        WHEN b.daralta THEN 'Finalizado/Alta'
        WHEN b.internar THEN 'Internado'
        WHEN b.ematendimento THEN 'Em atendimento'
        WHEN b.transferido THEN 'Transferido'
        ELSE 'Em aberto'
    END as status
FROM bam b
LEFT JOIN pacientes p ON b.paciente_idpaciente = p.idpaciente
LEFT JOIN avaliacao a ON b.avaliacao_idavaliacao = a.idavaliacao
LEFT JOIN prescricao pr ON b.idbam = pr.bam AND pr.prescricao IS NOT NULL AND pr.prescricao != ''
WHERE UPPER(p.nome) LIKE UPPER(%s)
GROUP BY b.idbam, b.controle, b.data, b.hora, b.datadaalta, b.unidade, b.natendente, b.receita, b.comentariotranferencia, b.transferido, b.daralta, b.ematendimento, b.internar, b.prioridade, p.nome, p.cpf, p.nascimento, p.sexo, p.telefone, p.endereco, p.bairro, p.municipio, p.mae, a.anamnese
ORDER BY b.data DESC, b.hora DESC
LIMIT 50
        """
        
        cursor.execute(query, (f'%{nome}%',))
        resultados = cursor.fetchall()
        
        if not resultados:
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'total': 0, 'resultados': []})
        
        # Converter para lista de dicionários
        pacientes = []
        for row in resultados:
            paciente = dict(row)
            # Converter tipos especiais para string
            for key, value in paciente.items():
                if value is not None:
                    paciente[key] = str(value)
            pacientes.append(paciente)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'total': len(pacientes),
            'resultados': pacientes
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gerar-pdf-bam/<int:idbam>', methods=['GET'])
def gerar_pdf_bam(idbam):
    """Gera PDF com os dados do paciente BAM"""
    # Início do corpo da função corrigido
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """
        SELECT 
            b.*,
            p.nome as paciente_nome,
            p.cpf as paciente_cpf,
            p.rg as paciente_rg,
            p.nascimento as paciente_nascimento,
            p.idade as paciente_idade,
            p.sexo as paciente_sexo,
            p.telefone as paciente_telefone,
            p.endereco as paciente_endereco,
            p.numero as paciente_numero,
            p.bairro as paciente_bairro,
            p.municipio as paciente_municipio,
            p.estado as paciente_estado,
            p.cep as paciente_cep,
            p.mae as paciente_mae,
            p.pai as paciente_pai,
            p.sangue as paciente_sangue,
            p.cns as paciente_cns,
            p.prontuario as paciente_prontuario,
            (
                SELECT string_agg(pr2.prescricao, '\n')
                FROM prescricao pr2
                WHERE pr2.bam = b.idbam AND pr2.prescricao IS NOT NULL AND pr2.prescricao != ''
            ) as prescricao,
            a.anamnese as avaliacao_anamnese,
            CASE 
                WHEN b.daralta THEN 'Finalizado/Alta'
                WHEN b.internar THEN 'Internado'
                WHEN b.ematendimento THEN 'Em atendimento'
                WHEN b.transferido THEN 'Transferido'
                ELSE 'Em aberto'
            END as status
        FROM bam b
        LEFT JOIN pacientes p ON b.paciente_idpaciente = p.idpaciente
        LEFT JOIN avaliacao a ON b.avaliacao_idavaliacao = a.idavaliacao
        WHERE b.idbam = %s
    """

        
    cursor.execute(query, (idbam,))
    dados = cursor.fetchone()
    if not dados:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Registro não encontrado'}), 404

    # Debug: printar dados retornados do banco
    print('DADOS DO BANCO:', dados)

    # Buscar prescrições/medicamentos
    query_prescricao = """
        SELECT prescricao, medicacao, observacao, data, hora
        FROM prescricao
        WHERE bam = %s
        ORDER BY idprescricao
    """
    cursor.execute(query_prescricao, (idbam,))
    prescricoes = cursor.fetchall()

    # Buscar exames
    query_exames = """
        SELECT relato, data, leito, enfermaria
        FROM examescomplementares
        WHERE nbam = %s
        ORDER BY idevolucao
    """
    cursor.execute(query_exames, (idbam,))
    exames = cursor.fetchall()

    # Criar PDF em memória
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1*cm, bottomMargin=1.5*cm)

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo para cabeçalho
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=1,  # Center
        spaceAfter=3
    )

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=10,
        alignment=1,  # Center
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        leading=11
    )

    # Conteúdo do PDF
    story = []

    # CABEÇALHO IGUAL AO EXEMPLO
    story.append(Paragraph("HOSPITAL MUNICIPAL LUIZ GONZAGA ( HMLG )", header_style))
    story.append(Paragraph(f"BOLETIM DE ATENDIMENTO MÉDICO: {dados['controle'] or 'N/A'}", small_style))

    # Linha com classificação, status e dados do atendimento
    classificacao_cor = "VERMELHO" if dados.get('prioridade') == '1' else "AMARELO" if dados.get('prioridade') == '2' else "VERDE"

    header_data = [
        [f"CLASSIFICAÇÃO DE RISCO: {classificacao_cor}", f"STATUS: {dados.get('status','N/A')}", f"SERVIÇO DE PRONTO SOCORRO"],
        [f"DATA: {dados['data'] or 'N/A'}", f"HORA: {dados['hora'] or 'N/A'}", ""],
        [f"CADASTRADO POR: {dados['natendente'] or 'N/A'}", "", ""]
    ]

    t_header = Table(header_data, colWidths=[7*cm, 5*cm, 6*cm])
    t_header.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('SPAN', (0, 2), (2, 2)),  # CADASTRADO POR ocupa as 3 colunas
        ('ALIGN', (0, 2), (2, 2), 'CENTER'),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 0.3*cm))

    # Dados do Paciente
    dados_paciente = [
        [f"NOME: {dados['paciente_nome'] or 'N/A'}", "", f"NASCIMENTO: {dados['paciente_nascimento'] or 'N/A'}"],
        [f"PROFISSÃO: N/A", f"SEXO: {dados['paciente_sexo'] or 'M'}", f"IDADE: {dados['paciente_idade'] or 'N/A'}"],
        [f"MÃE: {dados['paciente_mae'] or 'N/A'}", "", f"PAI: {dados['paciente_pai'] or 'N/A'}"],
        [f"PRONTUÁRIO ÚNICO: {dados['paciente_prontuario'] or 'N/A'}", "", f"CNS: {dados['paciente_cns'] or 'N/A'}"],
        [f"CPF: {dados['paciente_cpf'] or 'N/A'}", "", f"RG: {dados['paciente_rg'] or 'N/A'}"],
        [f"ESTADO CIVIL: N/A", "", f"NATURALIDADE: {dados['paciente_estado'] or 'N/A'}"],
        [f"ENDEREÇO: {dados['paciente_endereco'] or 'N/A'}", "", f"NÚMERO: {dados['paciente_numero'] or 'S/N'}"],
        [f"MUNICÍPIO: {dados['paciente_municipio'] or 'N/A'}", f"BAIRRO: {dados['paciente_bairro'] or 'N/A'}", f"CEP: {dados['paciente_cep'] or 'N/A'}"],
        [f"TELEFONES: {dados['paciente_telefone'] or 'N/A'}", "", f"SANGUE: {dados['paciente_sangue'] or 'N/A'}"]
    ]

    t1 = Table(dados_paciente, colWidths=[7*cm, 5*cm, 6*cm])
    t1.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (1, 0)),  # Nome ocupa 2 colunas
        ('SPAN', (0, 2), (1, 2)),  # Mãe ocupa 2 colunas
        ('SPAN', (0, 3), (1, 3)),  # Prontuário ocupa 2 colunas
        ('SPAN', (0, 4), (1, 4)),  # CPF ocupa 2 colunas
        ('SPAN', (0, 6), (1, 6)),  # Endereço ocupa 2 colunas
        ('SPAN', (0, 8), (1, 8)),  # Telefone ocupa 2 colunas
    ]))
    story.append(t1)
    story.append(Spacer(1, 0.3*cm))
    
    # ANAMNESE / QUEIXA PRINCIPAL
    if dados['avaliacao_anamnese'] or (dados.get('prescricao') and dados.get('prescricao').strip()):
        story.append(Paragraph("ANAMNESE / Exames Solicitados / Diagnóstico Provisório / Prescrição Inicial", heading_style))
        if dados['avaliacao_anamnese']:
            anamnese_text = (dados['avaliacao_anamnese'] or '').replace('\n', '<br/>')
            story.append(Paragraph(anamnese_text, small_style))
        # Prescrição principal (igual ao frontend)
        if dados.get('prescricao') and dados.get('prescricao').strip():
            story.append(Spacer(1, 0.2*cm))
            story.append(Paragraph("💊 Prescrição", ParagraphStyle('PrescricaoTitle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#764ba2'), fontName='Helvetica-Bold', spaceAfter=6)))
            prescricao_text = (dados['prescricao'] or '').replace('\n', '<br/>')
            story.append(Paragraph(prescricao_text, small_style))
        story.append(Spacer(1, 0.3*cm))

    # EXAMES REALIZADOS
    if exames:
        story.append(Paragraph("EXAMES SOLICITADOS / REALIZADOS", heading_style))
        exames_data = [['Relato', 'Data', 'Leito', 'Enfermaria']]
        for exame in exames:
            exames_data.append([
                exame['relato'] or 'N/A',
                str(exame['data']) if exame['data'] else 'N/A',
                exame['leito'] or 'N/A',
                exame['enfermaria'] or 'N/A'
            ])
        t_exames = Table(exames_data, colWidths=[8*cm, 4*cm, 3*cm, 3*cm])
        t_exames.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        story.append(t_exames)
        story.append(Spacer(1, 0.3*cm))

    # # PRESCRIÇÃO INICIAL / MEDICAMENTOS
    # if prescricoes:
    #     story.append(Paragraph("PRESCRIÇÃO INICIAL / MEDICAMENTOS ADMINISTRADOS", heading_style))
    #     prescricao_data = [['Prescrição', 'Medicação', 'Observação', 'Data', 'Hora']]
    #     for presc in prescricoes:
    #         prescricao_data.append([
    #             presc.get('prescricao', 'N/A') or 'N/A',
    #             presc.get('medicacao', 'N/A') or 'N/A',
    #             presc.get('observacao', 'N/A') or 'N/A',
    #             str(presc.get('data', 'N/A')) if presc.get('data') else 'N/A',
    #             str(presc.get('hora', 'N/A')) if presc.get('hora') else 'N/A',
    #         ])
    #     t_prescricao = Table(prescricao_data, colWidths=[5*cm, 5*cm, 5*cm, 2.5*cm, 2.5*cm])
    #     t_prescricao.setStyle(TableStyle([
    #         ('FONTSIZE', (0, 0), (-1, -1), 9),
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    #         ('TOPPADDING', (0, 0), (-1, -1), 6),
    #         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    #     ]))
    #     story.append(t_prescricao)
    #     story.append(Spacer(1, 0.3*cm))

    # Comentário de Transferência
    if dados['comentariotranferencia']:
        story.append(Paragraph("COMENTÁRIO DE TRANSFERÊNCIA", heading_style))
        comentario_text = (dados['comentariotranferencia'] or '').replace('\n', '<br/>')
        story.append(Paragraph(comentario_text, small_style))
        story.append(Spacer(1, 0.3*cm))

    # Rodapé - Local e Data
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("RIO DE JANEIRO", header_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"{dados['natendente'] or 'Atendente não identificado'} - CRM: {dados['controle'] or 'N/A'}", small_style))

    # Construir PDF
    doc.build(story)
    buffer.seek(0)

    cursor.close()
    conn.close()

    # Retornar PDF
    nome_arquivo = f"BAM_{dados['paciente_nome'].replace(' ', '_')}_{dados['controle']}.pdf"
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=nome_arquivo
    )

    # Fim da função

def limpar_html(texto):
    if not texto:
        return ''
    # Remove tags problemáticas e atributos
    texto = re.sub(r'<img[^>]*>', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'<(html|head|title|center|font|hr|b|h3|h4|h1|h2|h5|h6)[^>]*>', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'</?(html|head|title|center|font|hr|b|h3|h4|h1|h2|h5|h6)>', '', texto, flags=re.IGNORECASE)
    # Remove atributos width, height, align, size
    texto = re.sub(r'\s(width|height|align|size)=["\']?[^\s>]+', '', texto, flags=re.IGNORECASE)
    # Remove qualquer tag que não seja <br>
    texto = re.sub(r'<(?!br\s*\/?>)[^>]+>', '', texto)
    # Remove entidades HTML desconhecidas
    texto = re.sub(r'&[a-zA-Z0-9#]+;', '', texto)
    # Remove múltiplos <br> seguidos
    texto = re.sub(r'(<br\s*\/?>\s*)+', '<br/>', texto)
    return texto.strip()

if __name__ == '__main__':
    # Rodar no IP da máquina para permitir acesso externo
    app.run(host='0.0.0.0', port=5000, debug=True)
