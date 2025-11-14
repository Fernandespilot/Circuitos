"""
🔧 Construtor Interativo de Circuitos Elétricos
Executar com: python run_circuit_builder.py
"""

import subprocess
import sys
import os

def run_circuit_builder():
    """Executa o construtor de circuitos na porta 8503"""
    
    print("🔧 Iniciando Construtor Interativo de Circuitos...")
    print("🌐 Acesse: http://localhost:8503")
    print("⚡ Para parar: Ctrl+C\n")
    
    try:
        # Executa o Streamlit com configurações otimizadas
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app_circuit_builder.py",
            "--server.port", "8503",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.enableCORS", "false"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n✅ Construtor de circuitos encerrado.")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(run_circuit_builder())
