# 🚀 DEPLOY NO RAILWAY - PASSO A PASSO COMPLETO

## 📝 PARTE 1: CRIAR REPOSITÓRIO NO GITHUB (1 minuto)

1. Acesse: **https://github.com/new**
2. Preencha:
   - **Repository name:** `hospital-bam`
   - **Description:** "Sistema de busca BAM do Hospital"
   - Marque **"Private"** (para manter privado) ou "Public"
   - **NÃO** marque nenhuma opção (README, .gitignore, etc)
3. Clique em **"Create repository"**
4. **DEIXE A PÁGINA ABERTA** - você vai precisar da URL

---

## 💻 PARTE 2: EXECUTAR COMANDOS NO POWERSHELL (2 minutos)

**COPIE E COLE ESTES COMANDOS UM POR VEZ:**

```powershell
# 1. Inicializar Git
cd c:\Users\Kchorro\Desktop\GHBAM
git init

# 2. Adicionar todos os arquivos (exceto os grandes)
git add .

# 3. Fazer o primeiro commit
git commit -m "Deploy inicial - Sistema BAM"

# 4. Adicionar seu repositório GitHub (SUBSTITUA pela URL do seu repo!)
git remote add origin https://github.com/SEU_USUARIO/hospital-bam.git

# 5. Enviar para o GitHub
git branch -M main
git push -u origin main
```

**⚠️ ATENÇÃO:** No comando 4, substitua `SEU_USUARIO` pelo seu usuário do GitHub!

**Exemplo:** 
```powershell
git remote add origin https://github.com/kchorro/hospital-bam.git
```

---

## 🚂 PARTE 3: DEPLOY NO RAILWAY (3 minutos)

### 3.1 - Criar conta/projeto:
1. Acesse: **https://railway.app**
2. Faça login com sua conta GitHub
3. Clique em **"New Project"**
4. Selecione **"Provision PostgreSQL"**
5. Um banco de dados será criado automaticamente! ✅

### 3.2 - Importar dados do banco:
1. Clique no card **"Postgres"**
2. Vá na aba **"Variables"**
3. Copie os valores de:
   - `PGHOST`
   - `PGPORT` 
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

4. **No PowerShell**, execute (substitua os valores):

```powershell
$env:PGPASSWORD="COLE_AQUI_O_PGPASSWORD"
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h PGHOST_AQUI -p PGPORT_AQUI -U PGUSER_AQUI -d PGDATABASE_AQUI -v c:\Users\Kchorro\Desktop\GHBAM\hospitalmp_export.backup
```

**Aguarde 2-5 minutos** - vai importar todas as tabelas!

### 3.3 - Deploy da API:
1. No projeto do Railway, clique em **"New"**
2. Selecione **"GitHub Repo"**
3. Escolha o repositório **"hospital-bam"** que você criou
4. Clique em **"Deploy Now"**

### 3.4 - Configurar variáveis:
1. Clique no card do serviço que foi criado
2. Vá na aba **"Variables"**
3. Clique em **"New Variable"** > **"Add Reference"**
4. Selecione **"DATABASE_URL"** do Postgres
5. Clique em **"Add"**

### 3.5 - Configurar domínio:
1. Vá na aba **"Settings"**
2. Role até **"Networking"**
3. Clique em **"Generate Domain"**
4. **COPIE A URL** (vai ser tipo: `hospital-bam-api-production.up.railway.app`)

---

## 🌐 PARTE 4: ATUALIZAR O FRONTEND (1 minuto)

1. Abra o arquivo **BuscaBAM.html**
2. Procure pela linha: `const API_URL = 'http://192.168.1.5:5000/api';`
3. Substitua por: `const API_URL = 'https://SUA_URL_DO_RAILWAY/api';`

**Exemplo:**
```javascript
const API_URL = 'https://hospital-bam-api-production.up.railway.app/api';
```

4. Salve o arquivo
5. **PRONTO!** Agora você pode compartilhar o **BuscaBAM.html** com quem quiser! 🎉

---

## ✅ RESULTADO FINAL:
- ✅ Banco PostgreSQL na nuvem
- ✅ API rodando 24/7 
- ✅ Não precisa do seu PC ligado
- ✅ Custo: **$0 a $3/mês** (Railway dá $5 grátis)
- ✅ Link para compartilhar: **BuscaBAM.html**

---

## 🆘 SE DER ERRO:

**"git não é reconhecido":**
```powershell
winget install Git.Git
```

**"Authentication failed" no push:**
- Use GitHub Desktop OU
- Configure token: https://github.com/settings/tokens

**"pg_restore não encontrado":**
- Adicione ao PATH: `C:\Program Files\PostgreSQL\17\bin`

---

## 📞 PRONTO PARA COMEÇAR?

**Execute os comandos da PARTE 2 e me avise se der algum erro!** 🚀
