# 🚀 DEPLOY MANUAL NO RENDER - GUIA RÁPIDO

## ✅ ARQUIVOS PRONTOS:
- `hospital-bam-deploy.zip` - Código da API
- `hospitalmp_export.backup` - Banco de dados (44 MB)

---

## 📝 PASSO 1: CRIAR CONTA NO RENDER

1. Acesse: **https://render.com**
2. Clique em **"Get Started for Free"**
3. Cadastre-se com email ou Google
4. Confirme seu email

---

## 💾 PASSO 2: CRIAR BANCO DE DADOS PostgreSQL

1. No Dashboard do Render, clique em **"New +"** (botão azul no canto)
2. Selecione **"PostgreSQL"**
3. Preencha:
   - **Name:** `hospital-bam-db`
   - **Database:** `hospitalmp`
   - **User:** `postgres`
   - **Region:** `Oregon (US West)`
   - **PostgreSQL Version:** `17` (ou mais recente)
   - **Instance Type:** **FREE** ⚡
4. Clique em **"Create Database"**
5. **AGUARDE** 2-3 minutos até o status ficar **"Available"** (verde)

---

## 📊 PASSO 3: IMPORTAR SEUS DADOS NO BANCO

### 3.1 - Pegar informações de conexão:
1. Na página do banco criado, clique na aba **"Info"**
2. Anote estas informações:
   - **Hostname** (ex: `dpg-xxxxx.oregon-postgres.render.com`)
   - **Port** (geralmente `5432`)
   - **Database** (`hospitalmp`)
   - **Username** (`postgres`)
   - **Password** (clique em "show" para ver)

### 3.2 - Importar o backup:
1. Abra o **PowerShell** no seu PC
2. Cole este comando (SUBSTITUA os valores):

```powershell
$env:PGPASSWORD="COLE_A_SENHA_AQUI"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h COLE_O_HOSTNAME_AQUI -U postgres -d hospitalmp -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

**Exemplo preenchido:**
```powershell
$env:PGPASSWORD="abc123xyz789"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h dpg-xxxxx.oregon-postgres.render.com -U postgres -d hospitalmp -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

3. Pressione **Enter** e aguarde (pode demorar 2-5 minutos)
4. Se aparecer "pg_restore: error: could not execute query: ERROR:  role "postgres" already exists", **IGNORE** - é normal!
5. O importante é ver mensagens tipo: "processando dados da tabela 'bam'"

---

## 🌐 PASSO 4: FAZER DEPLOY DA API

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Escolha **"Deploy an existing image from a registry"**? **NÃO!** Clique em **"Next"**
4. Escolha **"Public Git repository"**? **NÃO!**
5. Role até o final e clique em **"Or deploy from a local directory"**

**ATENÇÃO:** O Render não permite upload direto de ZIP no plano FREE via interface!

### Solução alternativa (mais fácil):

1. Vá em: **https://dashboard.render.com/select-repo?type=web**
2. Role até o final e clique em **"+ Public Git Repository"**
3. Cole esta URL: `https://github.com/render-examples/flask-hello-world`
4. Clique em **"Connect"**
5. Configure:
   - **Name:** `hospital-bam-api`
   - **Region:** `Oregon (US West)`
   - **Branch:** `main`
   - **Root Directory:** deixe vazio
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api.app:app`
   - **Instance Type:** **FREE** ⚡

6. Em **"Environment Variables"**, clique **"Add Environment Variable"** e adicione:
   - **Key:** `DATABASE_URL`
   - **Value:** Volte na página do banco PostgreSQL, copie a **"External Database URL"** completa

7. Clique em **"Create Web Service"**
8. **AGUARDE** uns 5-10 minutos enquanto faz o deploy

---

## 🔧 PASSO 5: SUBSTITUIR O CÓDIGO

1. Após o deploy inicial terminar, vá na aba **"Shell"** do seu Web Service
2. Execute:
```bash
cd /opt/render/project/src
rm -rf *
```

**PROBLEMA:** Render FREE não permite upload manual! 😞

---

## 🎯 SOLUÇÃO MAIS FÁCIL: USAR RAILWAY

O **Railway** é MUITO mais simples para deploy manual:

1. Acesse: **https://railway.app**
2. Cadastre-se (pode usar GitHub)
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"** ou **"Empty Project"**
5. **Upload direto do ZIP!**

**Quer que eu faça o guia completo para o Railway? É MUITO mais fácil!** 🚀

---

## 💡 RECOMENDAÇÃO FINAL:

Como o Render não permite upload de ZIP no plano FREE, você tem 2 opções:

### OPÇÃO A - GITHUB (5 minutos)
1. Criar conta no GitHub (grátis)
2. Eu crio o repositório pra você
3. Deploy automático no Render
4. **MAIS FÁCIL E PROFISSIONAL**

### OPÇÃO B - RAILWAY (3 minutos)
1. Cadastrar no Railway
2. Upload do ZIP direto
3. Pronto!
4. **MAIS RÁPIDO**

**O que você prefere? GitHub ou Railway?**
