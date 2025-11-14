# 🧮 EXEMPLOS PRÁTICOS DE CÁLCULO - ANALISADOR RLC PRO
## 📊 Casos Práticos para Demonstração em Sala de Aula

---

## 🔍 **EXEMPLO 1: CIRCUITO RLC SÉRIE - ANÁLISE COMPLETA**

### **Dados de Entrada**
- **Frequência**: f = 60 Hz
- **Tensão RMS**: V = 220 V ∠ 0°
- **Resistência**: R = 10 Ω
- **Indutância**: L = 0.01 H (10 mH)
- **Capacitância**: C = 100 μF

### **Passo 1: Cálculo das Reatâncias**
```python
import math

f = 60  # Hz
L = 0.01  # H
C = 100e-6  # F

# Reatância Indutiva
XL = 2 * math.pi * f * L
XL = 2 * math.pi * 60 * 0.01
XL = 3.77 Ω

# Reatância Capacitiva  
XC = 1 / (2 * math.pi * f * C)
XC = 1 / (2 * math.pi * 60 * 100e-6)
XC = 26.53 Ω
```

### **Passo 2: Impedância Total**
```python
import cmath

R = 10  # Ω
X = XL - XC = 3.77 - 26.53 = -22.76 Ω  # Capacitivo

# Impedância complexa
Z = complex(R, X)
Z = 10 - j22.76 Ω

# Módulo e fase
|Z| = sqrt(R² + X²) = sqrt(10² + 22.76²) = 24.89 Ω
φ = arctan(X/R) = arctan(-22.76/10) = -66.3°
```

### **Passo 3: Corrente do Circuito**
```python
V = 220  # V (RMS)
I = V / |Z| = 220 / 24.89 = 8.84 A

# Ângulo da corrente
θ_i = 0° - (-66.3°) = +66.3°  # Corrente adiantada (capacitivo)
```

### **Passo 4: Tensões nos Componentes**
```python
VR = I × R = 8.84 × 10 = 88.4 V
VL = I × XL = 8.84 × 3.77 = 33.3 V  
VC = I × XC = 8.84 × 26.53 = 234.5 V

# Verificação: VR² + (VL - VC)² = V²
# 88.4² + (33.3 - 234.5)² = 88.4² + (-201.2)² = 7814 + 40481 = 48295
# V² = 220² = 48400 ✓ (pequena diferença por arredondamento)
```

### **Passo 5: Análise de Potências**
```python
# Potência Ativa
P = I² × R = 8.84² × 10 = 781.5 W

# Potência Reativa
Q = I² × X = 8.84² × (-22.76) = -1780.6 VAr  # Capacitivo

# Potência Aparente
S = V × I = 220 × 8.84 = 1944.8 VA

# Fator de Potência
FP = cos(φ) = cos(-66.3°) = 0.402  # Atrasado
```

### **🎯 Resultado do Código:**
```
🔷 RLC SÉRIE - CÁLCULOS DETALHADOS
═══════════════════════════════════════════════════════════════════════════════

📐 FÓRMULAS E CÁLCULOS:

1️⃣ REATÂNCIAS:
   XL = 2πfL = 2π × 60 × 0.0100 = 3.77 Ω
   XC = 1/(2πfC) = 1/(2π × 60 × 0.000100) = 26.53 Ω
   X = XL - XC = 3.77 - 26.53 = -22.76 Ω

2️⃣ IMPEDÂNCIA TOTAL:
   Z = R + jX = 10.0 + j(-22.76) Ω
   |Z| = √(R² + X²) = √(10.0² + -22.76²) = 24.89 Ω
   θ = arctan(X/R) = arctan(-22.76/10.0) = -66.3°

3️⃣ CORRENTE:
   I = V/Z = 220.0/24.89 = 8.840 A
   Ângulo da corrente = 0° - -66.3° = 66.3°
```

---

## 🔍 **EXEMPLO 2: ANÁLISE TRANSITÓRIA - RESPOSTA AO DEGRAU**

### **Dados de Entrada**
- **R = 100 Ω**, **L = 0.01 H**, **C = 1 μF**
- **Tensão do degrau**: V = 12 V
- **Condições iniciais**: iL(0) = 0, vC(0) = 0

### **Passo 1: Parâmetros do Sistema**
```python
import math

R = 100  # Ω
L = 0.01  # H  
C = 1e-6  # F

# Frequência natural
omega_n = 1 / math.sqrt(L * C)
omega_n = 1 / math.sqrt(0.01 * 1e-6) = 1 / math.sqrt(1e-8) = 1 / 1e-4 = 10000 rad/s

# Coeficiente de amortecimento
zeta = (R / 2) * math.sqrt(C / L)
zeta = (100 / 2) * math.sqrt(1e-6 / 0.01) = 50 * math.sqrt(1e-4) = 50 * 0.01 = 0.5
```

### **Passo 2: Determinação do Regime**
```python
if zeta < 1:
    regime = "Subamortecido"
    # Frequência amortecida
    omega_d = omega_n * math.sqrt(1 - zeta**2)
    omega_d = 10000 * math.sqrt(1 - 0.5**2) = 10000 * 0.866 = 8660 rad/s
```

### **Passo 3: Equações da Resposta (Subamortecido)**
```python
import numpy as np

def step_response(t, V, zeta, omega_n, omega_d):
    # Tensão no capacitor
    vc = V * (1 - np.exp(-zeta * omega_n * t) * 
              (np.cos(omega_d * t) + (zeta * omega_n / omega_d) * np.sin(omega_d * t)))
    
    # Corrente no indutor
    il = (V * omega_n**2 * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t)) / (L * omega_d)
    
    return vc, il

# Exemplo para t = 0.5 ms
t = 0.0005  # s
vc, il = step_response(t, 12, 0.5, 10000, 8660)
```

### **🎯 Resultado Esperado:**
- **Comportamento**: Oscilação amortecida
- **Período de oscilação**: T = 2π/ωd = 2π/8660 = 0.725 ms
- **Tempo de assentamento**: ts ≈ 4/(ζωn) = 4/(0.5×10000) = 0.8 ms

---

## 🔍 **EXEMPLO 3: ANÁLISE DE FREQUÊNCIA - DIAGRAMA DE BODE**

### **Dados de Entrada**
- **Circuito**: R = 1 kΩ, L = 10 mH, C = 1 μF
- **Função de Transferência**: H(s) = 1/(1 + sRC + s²LC)
- **Faixa**: 1 Hz a 100 kHz

### **Passo 1: Função de Transferência**
```python
import numpy as np

def transfer_function(f, R, L, C):
    omega = 2 * np.pi * f
    s = 1j * omega
    H = 1 / (1 + s * R * C + s**2 * L * C)
    return H

# Parâmetros
R = 1000  # Ω
L = 0.01  # H
C = 1e-6  # F

# Frequência de corte teórica
f_c = 1 / (2 * np.pi * R * C) = 1 / (2 * np.pi * 1000 * 1e-6) = 159.15 Hz
```

### **Passo 2: Cálculo da Resposta**
```python
# Vetor de frequência logarítmico
f = np.logspace(0, 5, 1000)  # 1 Hz a 100 kHz

# Resposta em frequência
H = transfer_function(f, R, L, C)

# Magnitude em dB
magnitude_db = 20 * np.log10(np.abs(H))

# Fase em graus  
phase_deg = np.degrees(np.angle(H))
```

### **Passo 3: Pontos Característicos**
```python
# Frequência de -3dB
idx_3db = np.argmin(np.abs(magnitude_db + 3))
f_3db = f[idx_3db]

# Frequência de ressonância (pico de magnitude)
idx_res = np.argmax(np.abs(H))
f_res = f[idx_res]

print(f"Frequência de -3dB: {f_3db:.2f} Hz")
print(f"Frequência de ressonância: {f_res:.2f} Hz") 
```

### **🎯 Características Esperadas:**
- **Tipo**: Filtro passa-baixa de 2ª ordem
- **Roll-off**: -40 dB/década após fc
- **Fase**: 0° → -90° → -180°
- **Frequência de corte**: ~159 Hz

---

## 🔍 **EXEMPLO 4: CORREÇÃO DE FATOR DE POTÊNCIA**

### **Problema**
Motor industrial consome 10 kW com FP = 0.7 atrasado em 220V/60Hz.  
**Objetivo**: Elevar FP para 0.95

### **Passo 1: Análise da Situação Atual**
```python
import math

P = 10000  # W (potência ativa)
fp_atual = 0.7
V = 220  # V (RMS)
f = 60  # Hz

# Ângulo atual
phi_atual = math.acos(fp_atual)  # 45.57°

# Potência reativa atual
Q_atual = P * math.tan(phi_atual)  # 10206 VAr

# Corrente atual
I_atual = P / (V * fp_atual)  # 64.94 A
```

### **Passo 2: Situação Desejada**
```python
fp_desejado = 0.95
phi_desejado = math.acos(fp_desejado)  # 18.19°

# Nova potência reativa
Q_desejado = P * math.tan(phi_desejado)  # 3287 VAr

# Redução necessária
Q_compensacao = Q_atual - Q_desejado  # 6919 VAr
```

### **Passo 3: Capacitor de Correção**
```python
# Capacitância necessária
C_correcao = Q_compensacao / (2 * math.pi * f * V**2)
C_correcao = 6919 / (2 * math.pi * 60 * 220**2)
C_correcao = 378.8e-6  # F = 378.8 μF

# Valor comercial mais próximo
C_comercial = 400e-6  # 400 μF
```

### **🎯 Resultado da Correção:**
```
📊 CORREÇÃO DE FATOR DE POTÊNCIA
═══════════════════════════════════════════════════════════════════════════════

🔋 SITUAÇÃO ATUAL:
• Potência ativa: 10.0 kW
• Fator de potência: 0.70
• Potência reativa: 10.2 kVAr  
• Corrente: 64.9 A

🎯 SITUAÇÃO DESEJADA:
• Fator de potência: 0.95
• Potência reativa: 3.3 kVAr
• Corrente: 47.6 A

⚡ CAPACITOR NECESSÁRIO:
• Redução de Q: 6.9 kVAr
• Capacitância: 379 μF
• Valor comercial: 400 μF

💡 BENEFÍCIOS:
• Redução da corrente: 26.6%
• Economia na demanda: R$ xxx/mês
• Melhoria da regulação: xx%
```

---

## 🔍 **EXEMPLO 5: CIRCUITO EM RESSONÂNCIA**

### **Condição de Ressonância**
XL = XC, ou seja, ωL = 1/(ωC)

### **Frequência de Ressonância**
```python
def frequencia_ressonancia(L, C):
    omega_r = 1 / math.sqrt(L * C)
    f_r = omega_r / (2 * math.pi)
    return f_r

# Exemplo
L = 0.1  # H
C = 10e-6  # F (10 μF)

f_r = frequencia_ressonancia(L, C)
f_r = 503.3 Hz
```

### **Características na Ressonância**
```python
# Na ressonância série:
# - Impedância mínima: Z = R
# - Corrente máxima: I = V/R  
# - Tensões VL e VC podem ser muito altas!
# - Fator de qualidade: Q = ωL/R = 1/(ωRC)

R = 10  # Ω
Q = (2 * math.pi * f_r * L) / R
Q = 31.6

# Tensões nos reativos (podem exceder a tensão da fonte!)
VL = VC = Q * V  # Se V = 10V, então VL = VC = 316V!
```

---

## 📚 **FORMULÁRIO DE REFERÊNCIA RÁPIDA**

### **Impedâncias Básicas**
```
Resistor:     ZR = R
Indutor:      ZL = jωL = jXL
Capacitor:    ZC = 1/(jωC) = -jXC
```

### **Circuito RLC Série**
```
Z = R + j(XL - XC)
I = V/Z
VR = IR,  VL = IXL,  VC = IXC
```

### **Circuito RLC Paralelo**  
```
Y = 1/R + 1/(jXL) + j/(XC)
I = VY
IR = V/R,  IL = V/XL,  IC = VωC
```

### **Potências**
```
P = VIcos(φ) = I²R        [W]
Q = VIsin(φ) = I²X        [VAr]  
S = VI = √(P² + Q²)       [VA]
FP = P/S = cos(φ)
```

### **Análise Transitória**
```
ωn = 1/√(LC)              [rad/s]
ζ = R/(2√(L/C))
Q = 1/(2ζ) = ωnL/R

ζ < 1: Subamortecido (oscila)
ζ = 1: Criticamente amortecido  
ζ > 1: Superamortecido
```

---

**🎓 Este documento serve como guia prático para demonstrar os cálculos implementados no código durante a apresentação em sala de aula.**
