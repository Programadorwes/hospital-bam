# 🚀 DEPLOY GRATUITO NO RENDER.COM

## 📋 PASSO A PASSO COMPLETO

### PARTE 1: CRIAR CONTA NO RENDER
1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Cadastre-se com seu email ou GitHub

### PARTE 2: SUBIR O BANCO DE DADOS (PostgreSQL)
1. No Dashboard do Render, clique em "New +"
2. Selecione "PostgreSQL"
3. Configure:
   - Name: `hospital-bam-db`
   - Database: `hospitalmp`
   - User: `postgres`
   - Region: `Oregon (US West)` (mais rápido pro Brasil)
   - **Plano: FREE**
4. Clique em "Create Database"
5. **AGUARDE** até aparecer "Available" (uns 2-3 minutos)

### PARTE 3: IMPORTAR SEUS DADOS
1. Na página do banco criado, vá em "Connect"
2. Copie o comando "PSQL Command" (vai ter algo assim):
   ```
   PGPASSWORD=xxxx psql -h dpg-xxxx-a.oregon-postgres.render.com -U postgres hospitalmp
   ```
3. Abra o PowerShell no seu PC
4. Cole o comando copiado (ele vai conectar no banco na nuvem)
5. Depois digite este comando para importar:
   ```
   \! pg_restore -d hospitalmp c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
   ```
   
   **OU use este método mais simples:**
   
   No PowerShell:
   ```powershell
   $env:PGPASSWORD="SENHA_DO_RENDER_AQUI"
   & "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h HOSTNAME_DO_RENDER -U postgres -d hospitalmp c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
   ```
   
   Substitua:
   - `SENHA_DO_RENDER_AQUI` pela senha que aparece no Render
   - `HOSTNAME_DO_RENDER` pelo host que aparece no Render (ex: dpg-xxxx.oregon-postgres.render.com)

### PARTE 4: SUBIR A API (Flask)
1. No Dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Escolha "Build and deploy from a Git repository"
4. Como você não tem GitHub, escolha "Public Git repository"
5. **OU** clique em "Deploy from GitHub" e conecte sua conta GitHub

   **OPÇÃO A - SEM GITHUB (mais fácil):**
   - Vou criar um arquivo ZIP para você fazer upload manual
   
   **OPÇÃO B - COM GITHUB (recomendado):**
   - Vou te ensinar a subir no GitHub primeiro

### PARTE 5: ATUALIZAR O FRONTEND
Depois que a API estiver no ar, você vai ter uma URL tipo:
`https://hospital-bam-api.onrender.com`

Você vai precisar atualizar o arquivo `BuscaBAM.html` para usar essa URL:
```javascript
const API_URL = 'https://hospital-bam-api.onrender.com/api';
```

---

## 🎯 QUAL CAMINHO VOCÊ QUER SEGUIR?

**OPÇÃO 1 - SEM GITHUB (Manual)**
- Vou criar um ZIP com tudo
- Você faz upload direto no Render
- Mais simples mas menos profissional

**OPÇÃO 2 - COM GITHUB (Recomendado)**
- Cria conta no GitHub (grátis)
- Sobe o código lá
- Render faz deploy automático
- Mais profissional e fácil de atualizar depois

---

## 📊 CUSTOS
- **PostgreSQL Free**: 90 dias grátis, depois $7/mês
- **Web Service Free**: 750 horas/mês grátis (suficiente!)
- **Limitação Free**: App "dorme" após 15min sem uso (demora ~1min pra acordar)

---

## 🔥 ALTERNATIVAS 100% GRÁTIS SEM LIMITAÇÃO:
Se quiser 100% grátis para sempre:
1. **Railway** - $5 grátis/mês (suficiente pra uso leve)
2. **PythonAnywhere** - Grátis mas só 1 app
3. **Vercel** (frontend) + **Supabase** (banco grátis) - Mais complexo

---

ME DIGA QUAL OPÇÃO VOCÊ QUER E EU TE AJUDO! 🚀
