# 🏥 Hospital BAM - Sistema de Busca de Pacientes

Sistema web para busca e geração de relatórios PDF de pacientes atendidos no BAM (Boletim de Atendimento Médico).

## 🚀 Tecnologias
- **Backend:** Python + Flask
- **Banco de Dados:** PostgreSQL
- **Frontend:** HTML + JavaScript
- **PDF:** ReportLab

## 📦 Deploy
Este projeto está configurado para deploy automático no Railway/Render.

## 🔧 Variáveis de Ambiente Necessárias
- `DATABASE_URL` - URL de conexão PostgreSQL

## 🏃 Como Rodar Localmente
```bash
pip install -r requirements.txt
cd api
python app.py
```

Acesse: `http://localhost:5000`

## 📄 Funcionalidades
- Busca de pacientes por nome
- Visualização de dados do BAM
- Geração de PDF com informações médicas
- Exibição de anamnese/SOAP
