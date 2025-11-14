@echo off
echo 🚀 Preparando deploy para Streamlit Cloud...

REM 1. Adicionar todos os arquivos ao Git
echo 📁 Adicionando arquivos...
git add .

REM 2. Commit com mensagem descritiva
echo 💾 Fazendo commit...
git commit -m "Deploy: Analisador de Circuitos RLC para estudantes - %date% %time%"

REM 3. Push para GitHub
echo 📤 Enviando para GitHub...
git push origin main

echo.
echo ✅ Deploy preparado!
echo.
echo 🌐 Próximos passos:
echo 1. Acesse: https://share.streamlit.io/
echo 2. Faça login com GitHub
echo 3. Clique em 'New app'
echo 4. Selecione o repositório: Fernandespilot/ConcursAI
echo 5. Escolha o arquivo: app.py
echo 6. Clique em 'Deploy'
echo.
echo 🎯 URLs sugeridas:
echo - app.py → https://circuitos-rlc-basico.streamlit.app/
echo - app_advanced.py → https://circuitos-rlc-avancado.streamlit.app/
echo - app_circuit_builder.py → https://circuitos-rlc-construtor.streamlit.app/

pause
