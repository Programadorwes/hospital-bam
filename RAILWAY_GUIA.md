# 🚂 DEPLOY GRÁTIS NO RAILWAY - SUPER SIMPLES!

## 🎯 POR QUE RAILWAY?
✅ Upload direto de arquivos (não precisa GitHub!)
✅ 100% grátis para começar ($5 de crédito/mês - suficiente!)
✅ Deploy em 5 minutos
✅ Mais fácil que Render

---

## 📝 PASSO 1: CRIAR CONTA NO RAILWAY

1. Acesse: **https://railway.app**
2. Clique em **"Login"** no canto superior
3. Escolha **"Login with Email"** ou **"Login with GitHub"**
4. Confirme seu email
5. No primeiro login, você ganha **$5 de crédito grátis/mês**

---

## 🗄️ PASSO 2: CRIAR O BANCO DE DADOS

1. No Dashboard, clique em **"New Project"**
2. Selecione **"Provision PostgreSQL"**
3. Pronto! O banco já está criado! ✨
4. Clique no card **"Postgres"** que apareceu
5. Vá na aba **"Variables"**
6. Anote estas informações (ou deixe a aba aberta):
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

---

## 📊 PASSO 3: IMPORTAR SEUS DADOS

1. Abra o **PowerShell** no seu PC
2. Cole este comando (SUBSTITUA os valores que você anotou):

```powershell
$env:PGPASSWORD="COLE_O_PGPASSWORD_AQUI"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h COLE_O_PGHOST_AQUI -p COLE_O_PGPORT_AQUI -U COLE_O_PGUSER_AQUI -d COLE_O_PGDATABASE_AQUI -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

**Exemplo preenchido:**
```powershell
$env:PGPASSWORD="abc123xyz"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h containers-us-west-123.railway.app -p 5432 -U postgres -d railway -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

3. Pressione **Enter** e aguarde (2-5 minutos)
4. Ignore erros sobre roles/permissions - é normal!
5. Procure por mensagens: "processando dados da tabela 'bam'" ✅

---

## 🚀 PASSO 4: FAZER DEPLOY DA API

### 4.1 - Criar o serviço:
1. No mesmo projeto, clique em **"New"** (botão roxo no canto)
2. Selecione **"Empty Service"**
3. Um novo card aparecerá

### 4.2 - Fazer upload do código:
1. Clique no card do novo serviço
2. Vá na aba **"Settings"**
3. Em **"Service Name"**, coloque: `hospital-bam-api`
4. Role até **"Source"** e clique em **"Connect to a GitHub repo"**

**PROBLEMA:** Railway também precisa de GitHub! 😅

---

## 🎯 SOLUÇÃO DEFINITIVA: USAR GITHUB (5 MINUTOS)

Vou criar o repositório GitHub pra você AGORA! É super rápido:

### O que eu vou fazer:
1. ✅ Criar estrutura de pastas correta
2. ✅ Preparar todos os arquivos
3. ✅ Te dar comandos prontos para copiar/colar

### O que VOCÊ vai fazer:
1. Criar conta no GitHub (30 segundos)
2. Criar repositório vazio (30 segundos)
3. Copiar/colar 3 comandos no PowerShell (1 minuto)
4. Conectar no Railway/Render (2 minutos)
5. **PRONTO! API NO AR!** 🎉

---

## 🤔 VOCÊ PREFERE:

### OPÇÃO A - Eu crio tudo no GitHub pra você
Você só copia/cola os comandos que eu te passar

### OPÇÃO B - Usamos PythonAnywhere
Upload direto de arquivos, sem GitHub
Limitação: só 1 app grátis

**Me diz qual você quer e eu faço AGORA! 🚀**
