@echo off
echo ========================================
echo 🚀 DEPLOY CIRCUIT ANALYZER PRO
echo Versão Completa - Todas Funcionalidades
echo ========================================

echo.
echo 📋 Verificando arquivos...
if exist "app_completo_online.py" (
    echo ✅ app_completo_online.py encontrado
) else (
    echo ❌ app_completo_online.py não encontrado!
    pause
    exit /b 1
)

if exist "requirements_completo.txt" (
    echo ✅ requirements_completo.txt encontrado
) else (
    echo ❌ requirements_completo.txt não encontrado!
    pause
    exit /b 1
)

echo.
echo 🔧 Adicionando arquivos ao Git...
git add app_completo_online.py
git add requirements_completo.txt
git add DEPLOY_COMPLETO.md

echo.
echo 💾 Fazendo commit...
git commit -m "Deploy: Circuit Analyzer PRO - Versão Completa com todas funcionalidades"

echo.
echo 🌐 Enviando para GitHub...
git push origin main

echo.
echo ========================================
echo ✅ DEPLOY CONCLUÍDO!
echo ========================================
echo.
echo 🚀 Próximos passos:
echo 1. Acesse: https://share.streamlit.io/
echo 2. Conecte seu GitHub (Fernandespilot/ConcursAI)
echo 3. Configure:
echo    - Repository: Fernandespilot/ConcursAI
echo    - Branch: main
echo    - Main file: app_completo_online.py
echo 4. Clique em "Deploy!"
echo.
echo 📱 URL final esperada:
echo https://circuit-analyzer-pro.streamlit.app/
echo.
echo 🎯 Funcionalidades incluídas:
echo ✅ Sinais Elétricos (gráficos interativos)
echo ✅ Diagramas Fasoriais (análise completa)
echo ✅ Designer de Circuitos
echo ✅ Análise Transitória (degrau/impulso)
echo ✅ Resposta em Frequência (Bode)
echo ✅ Diagrama de Nyquist
echo ✅ Relatórios (download CSV)
echo.
echo 🔥 Aplicação rodando localmente em:
echo http://localhost:8520
echo ========================================

pause
