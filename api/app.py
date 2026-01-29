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

app = Flask(__name__)
CORS(app)

# Configurações do banco - usa variável de ambiente ou local
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Render usa postgresql:// mas psycopg2 precisa de postgres://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
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
                a.anamnese as avaliacao_anamnese
            FROM bam b
            LEFT JOIN pacientes p ON b.paciente_idpaciente = p.idpaciente
            LEFT JOIN avaliacao a ON b.avaliacao_idavaliacao = a.idavaliacao
            WHERE UPPER(p.nome) LIKE UPPER(%s)
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Buscar dados completos
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
                a.anamnese as avaliacao_anamnese
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
        
        # Criar PDF em memória
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=20,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        # Conteúdo do PDF
        story = []
        
        # Título
        story.append(Paragraph("FICHA DE ATENDIMENTO - BAM", title_style))
        story.append(Paragraph(f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
        
        # Dados do Paciente
        story.append(Paragraph("DADOS DO PACIENTE", heading_style))
        dados_paciente = [
            ['Nome:', dados['paciente_nome'] or 'N/A'],
            ['CPF:', dados['paciente_cpf'] or 'N/A'],
            ['RG:', dados['paciente_rg'] or 'N/A'],
            ['Data Nascimento:', dados['paciente_nascimento'] or 'N/A'],
            ['Idade:', dados['paciente_idade'] or 'N/A'],
            ['Sexo:', dados['paciente_sexo'] or 'N/A'],
            ['Tipo Sanguíneo:', dados['paciente_sangue'] or 'N/A'],
            ['Telefone:', dados['paciente_telefone'] or 'N/A'],
        ]
        
        t1 = Table(dados_paciente, colWidths=[5*cm, 12*cm])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t1)
        story.append(Spacer(1, 0.5*cm))
        
        # Endereço
        story.append(Paragraph("ENDEREÇO", heading_style))
        endereco = f"{dados['paciente_endereco'] or ''}, {dados['paciente_numero'] or 'S/N'}"
        bairro_cidade = f"{dados['paciente_bairro'] or ''} - {dados['paciente_municipio'] or ''}/{dados['paciente_estado'] or ''}"
        cep = f"CEP: {dados['paciente_cep'] or 'N/A'}"
        
        dados_endereco = [
            ['Endereço:', endereco],
            ['Bairro/Cidade:', bairro_cidade],
            ['CEP:', dados['paciente_cep'] or 'N/A']
        ]
        
        t2 = Table(dados_endereco, colWidths=[5*cm, 12*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.5*cm))
        
        # Dados do Atendimento
        story.append(Paragraph("DADOS DO ATENDIMENTO", heading_style))
        dados_atendimento = [
            ['Controle:', dados['controle'] or 'N/A'],
            ['Data Atendimento:', dados['data'] or 'N/A'],
            ['Hora:', dados['hora'] or 'N/A'],
            ['Unidade:', dados['unidade'] or 'N/A'],
            ['Atendente:', dados['natendente'] or 'N/A'],
            ['Prioridade:', dados['prioridade'] or 'N/A'],
            ['Em Atendimento:', 'Sim' if dados['ematendimento'] else 'Não'],
            ['Internar:', 'Sim' if dados['internar'] else 'Não'],
            ['Data da Alta:', dados['datadaalta'] or 'N/A'],
            ['Dar Alta:', 'Sim' if dados['daralta'] else 'Não'],
            ['Transferido:', 'Sim' if dados['transferido'] else 'Não'],
        ]
        
        t3 = Table(dados_atendimento, colWidths=[5*cm, 12*cm])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t3)
        story.append(Spacer(1, 0.5*cm))
        
        # ANAMNESE / SOAP DO MÉDICO
        if dados['avaliacao_anamnese']:
            story.append(Paragraph("RELATO MÉDICO / SOAP", heading_style))
            anamnese_text = dados['avaliacao_anamnese'].replace('\n', '<br/>')
            story.append(Paragraph(anamnese_text, styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
        
        # Receita/Prescrição
        if dados['receita']:
            story.append(Paragraph("RECEITA/PRESCRIÇÃO", heading_style))
            receita_text = dados['receita'].replace('\n', '<br/>')
            story.append(Paragraph(receita_text, styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
        
        # Comentário de Transferência
        if dados['comentariotranferencia']:
            story.append(Paragraph("COMENTÁRIO DE TRANSFERÊNCIA", heading_style))
            comentario_text = dados['comentariotranferencia'].replace('\n', '<br/>')
            story.append(Paragraph(comentario_text, styles['Normal']))
        
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
            as_attachment=True,
            download_name=nome_arquivo
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Rodar no IP da máquina para permitir acesso externo
    app.run(host='0.0.0.0', port=5000, debug=True)
