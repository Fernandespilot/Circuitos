#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar os gráficos de resposta em frequência
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkTk
import tkinter as tk

def test_magnitude_response():
    """Teste simples de resposta em magnitude"""
    print("🔍 Testando gráficos de resposta em magnitude...")
    
    # Parâmetros do circuito RLC
    R = 100  # Ohm
    L = 0.01  # Henry
    C = 1e-6  # Farad
    
    # Faixa de frequência
    f = np.logspace(1, 5, 1000)  # 10 Hz a 100 kHz
    w = 2 * np.pi * f
    
    # Função de transferência H(jw) = 1 / (1 + jwRC + (jw)²LC)
    s = 1j * w
    H = 1 / (1 + s*R*C + (s**2)*L*C)
    
    # Magnitude e fase
    magnitude = np.abs(H)
    magnitude_db = 20 * np.log10(magnitude)
    phase_deg = np.degrees(np.angle(H))
    
    # Criar gráficos
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Gráfico de magnitude
    ax1.semilogx(f, magnitude, 'b-', linewidth=2, label='|H(jω)|')
    ax1.axhline(y=1/np.sqrt(2), color='r', linestyle='--', label='-3dB')
    ax1.set_xlabel('Frequência [Hz]')
    ax1.set_ylabel('Magnitude')
    ax1.set_title('Resposta em Magnitude')
    ax1.grid(True)
    ax1.legend()
    
    # Gráfico de fase
    ax2.semilogx(f, phase_deg, 'g-', linewidth=2, label='∠H(jω)')
    ax2.axhline(y=-45, color='r', linestyle='--', label='-45°')
    ax2.set_xlabel('Frequência [Hz]')
    ax2.set_ylabel('Fase [°]')
    ax2.set_title('Resposta em Fase')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Teste concluído com sucesso!")
    
    # Estatísticas
    f_3db_idx = np.argmin(np.abs(magnitude - 1/np.sqrt(2)))
    f_3db = f[f_3db_idx]
    
    print(f"""
📊 RESULTADOS DO TESTE:
• Frequência de corte (-3dB): {f_3db:.2f} Hz
• Magnitude máxima: {np.max(magnitude):.3f}
• Magnitude mínima: {np.min(magnitude):.6f}
• Fase inicial: {phase_deg[0]:.1f}°
• Fase final: {phase_deg[-1]:.1f}°
""")
    
    return magnitude, phase_deg, f

if __name__ == "__main__":
    test_magnitude_response()
