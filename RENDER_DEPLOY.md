# 🚀 DEPLOY NO RENDER - GUIA COMPLETO

## ✅ PARTE 1: CRIAR BANCO DE DADOS PostgreSQL (3 minutos)

1. Acesse: **https://dashboard.render.com**
2. Faça login com seu GitHub
3. Clique em **"New +"** (botão azul no topo)
4. Selecione **"PostgreSQL"**
5. Preencha:
   - **Name:** `hospital-bam-db`
   - **Database:** `hospitalmp`
   - **User:** `postgres`
   - **Region:** `Oregon (US West)` (mais rápido para o Brasil)
   - **PostgreSQL Version:** `17`
   - **Instance Type:** **FREE** ⚡
6. Clique em **"Create Database"**
7. **AGUARDE** 2-3 minutos até aparecer **"Available"** (fica verde)

---

## 📊 PARTE 2: IMPORTAR DADOS DO BANCO (5 minutos)

### 2.1 - Pegar informações de conexão:
1. Na página do banco criado, vá na aba **"Info"**
2. Role até **"Connections"**
3. Copie o valor de **"External Database URL"** (começa com `postgres://`)
   
   **OU anote separadamente:**
   - **Hostname**
   - **Port**
   - **Database**
   - **Username** 
   - **Password** (clique em 👁️ para ver)

### 2.2 - Importar no PowerShell:

**OPÇÃO A - URL completa:**
```powershell
$env:DATABASE_URL="COLE_A_EXTERNAL_DATABASE_URL_AQUI"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -d $env:DATABASE_URL -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

**OPÇÃO B - Dados separados:**
```powershell
$env:PGPASSWORD="COLE_PASSWORD_AQUI"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h HOSTNAME_AQUI -p PORT_AQUI -U USERNAME_AQUI -d DATABASE_AQUI -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

3. Aguarde 2-5 minutos (vai mostrar: "processando dados da tabela 'bam'...")
4. **Ignore** erros sobre "role already exists" - é normal!
5. Quando terminar, volta pro Dashboard do Render

---

## 🌐 PARTE 3: FAZER DEPLOY DA API (5 minutos)

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Clique em **"Build and deploy from a Git repository"**
4. Clique em **"Connect a repository"** ou **"Configure account"**
5. Autorize o Render a acessar seu GitHub
6. Na lista, selecione **"hospital-bam"**
7. Clique em **"Connect"**

### 3.1 - Configurar o serviço:
Preencha EXATAMENTE assim:

- **Name:** `hospital-bam-api`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** deixe vazio
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn api.app:app`
- **Instance Type:** **FREE** ⚡

### 3.2 - Adicionar variável de ambiente:
1. Role até **"Environment Variables"**
2. Clique em **"Add Environment Variable"**
3. Preencha:
   - **Key:** `DATABASE_URL`
   - **Value:** Cole a **"Internal Database URL"** do banco PostgreSQL
     (volte na aba do banco → Info → Internal Database URL)

### 3.3 - Criar serviço:
1. Clique em **"Create Web Service"**
2. **AGUARDE** 5-10 minutos (vai aparecer "Live" quando terminar)
3. Você vai ver os logs do deploy acontecendo

---

## 🎯 PARTE 4: PEGAR A URL DA API

1. Quando aparecer **"Live"** (verde), copie a URL no topo
2. Vai ser algo como: `https://hospital-bam-api.onrender.com`
3. **ANOTE ESSA URL!**

---

## 🔧 PARTE 5: ATUALIZAR O FRONTEND

Agora você precisa atualizar o arquivo BuscaBAM.html para usar a nova URL.

**Me avisa quando chegar aqui que eu atualizo o arquivo pra você!** ✅

---

## 🎉 RESULTADO FINAL:

✅ Banco PostgreSQL na nuvem  
✅ API rodando 24/7 sem depender do seu PC  
✅ URL pública para compartilhar  
✅ Deploy automático a cada `git push`  
✅ **100% GRÁTIS** (750 horas/mês no plano FREE)  

---

## ⚠️ LIMITAÇÃO DO PLANO FREE:
- O serviço **"dorme"** após 15 minutos sem uso
- **Demora ~1 minuto** para "acordar" no primeiro acesso
- Depois fica normal!

---

## 🆘 SE DER PROBLEMA:

**"Build failed":**
- Verifique se o `requirements.txt` está correto
- Verifique se o Start Command é `gunicorn api.app:app`

**"Application error":**
- Vá em "Logs" e me manda o erro
- Provavelmente é a DATABASE_URL

**Banco não importou:**
- Verifique se usou a URL/senha correta
- Tente novamente o comando pg_restore

---

**COMECE PELA PARTE 1 e me avisa em qual passo você está! 🚀**
