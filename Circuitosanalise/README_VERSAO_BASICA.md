# ⚡ ANALISADOR DE CIRCUITOS RLC - VERSÃO BÁSICA
## 🎓 Interface Educacional Simplificada

### **🚀 Acesso Direto Online:**
**Link da Aplicação**: https://circuitos-rlc-basico.streamlit.app/

---

## 📖 **O QUE É ESTE APLICATIVO**

Uma ferramenta educacional interativa para análise de circuitos elétricos RLC (Resistor-Indutor-Capacitor) desenvolvida especificamente para estudantes de engenharia.

### **🎯 Objetivos Educacionais:**
- Facilitar o aprendizado de conceitos de circuitos AC
- Visualizar comportamento de sinais senoidais
- Compreender análise fasorial
- Calcular potências e fator de potência
- Validar cálculos manuais

---

## 🔧 **FUNCIONALIDADES PRINCIPAIS**

### **📊 Parâmetros de Entrada:**
- **Frequência** (Hz): Frequência da rede elétrica
- **Tensão Máxima** (V): Amplitude do sinal de tensão
- **Corrente Máxima** (A): Amplitude do sinal de corrente
- **Ângulo da Tensão** (°): Fase inicial da tensão
- **Ângulo da Corrente** (°): Fase inicial da corrente

### **📈 Análises Disponíveis:**
1. **Formas de Onda**: v(t), i(t), p(t)
2. **Diagramas Fasoriais**: Representação vetorial
3. **Cálculos de Potência**: P, Q, S, FP
4. **Valores RMS**: Tensão e corrente eficazes
5. **Correção de Fator de Potência**: Cálculo automático

---

## 🧮 **EXEMPLO DE USO**

### **Caso Prático - Circuito Residencial:**
```
Parâmetros:
- Frequência: 60 Hz
- Tensão Máxima: 311 V (220 VRMS)
- Corrente Máxima: 10 A
- Ângulo Tensão: 0°
- Ângulo Corrente: -30° (indutivo)

Resultados:
- Tensão RMS: 220 V
- Corrente RMS: 7.07 A
- Fator de Potência: 0.866 (atrasado)
- Potência Ativa: 1348 W
```

---

## 👨‍🎓 **PARA ESTUDANTES**

### **Como Usar:**
1. 📱 Abra o link no navegador (funciona no celular!)
2. 🎛️ Ajuste os parâmetros na barra lateral
3. 📊 Observe os gráficos atualizando em tempo real
4. 🧮 Compare com seus cálculos manuais
5. 📋 Use o relatório para documentar resultados

### **Dicas de Estudo:**
- Teste diferentes valores e observe os efeitos
- Compare circuitos resistivos, indutivos e capacitivos
- Experimente correção de fator de potência
- Use os presets rápidos para casos comuns

---

## 👨‍🏫 **PARA PROFESSORES**

### **Aplicações em Aula:**
- **Demonstrações interativas** de conceitos teóricos
- **Validação de exercícios** resolvidos em classe
- **Experimentos virtuais** sem necessidade de laboratório
- **Visualização de conceitos abstratos** como fasores

### **Conceitos Abordados:**
- Valores eficazes (RMS)
- Análise fasorial
- Potência em circuitos AC
- Fator de potência
- Defasagem entre tensão e corrente

---

## 🔬 **BASE CIENTÍFICA**

### **Equações Implementadas:**
```
Valores RMS:
Vrms = Vmax / √2
Irms = Imax / √2

Potências:
P = Vrms × Irms × cos(φ)  [Watts]
Q = Vrms × Irms × sin(φ)  [VAr]
S = Vrms × Irms           [VA]

Fator de Potência:
FP = cos(φ) = P/S
```

### **Sinais Temporais:**
```python
v(t) = Vmax × sin(ωt + θv)
i(t) = Imax × sin(ωt + θi)
p(t) = v(t) × i(t)
```

---

## 🌐 **REQUISITOS TÉCNICOS**

### **Para Usar Online:**
- ✅ Qualquer navegador moderno
- ✅ Conexão com internet
- ✅ Funciona em desktop, tablet e smartphone
- ❌ Não precisa instalar nada

### **Para Executar Localmente:**
```bash
pip install streamlit numpy pandas plotly matplotlib
streamlit run app.py
```

---

## 📚 **MATERIAL COMPLEMENTAR**

### **Documentação Técnica:**
- [📋 Relatório Técnico Completo](./nova-versao-visual/RELATORIO_COMPLETO_PARA_AULA.md)
- [🧮 Exemplos Práticos](./nova-versao-visual/EXEMPLOS_PRATICOS_CALCULOS.md)
- [🎤 Guia de Apresentação](./nova-versao-visual/RESUMO_EXECUTIVO_APRESENTACAO.md)

### **Versões Mais Avançadas:**
- [⚙️ Versão Avançada](https://circuitos-rlc-avancado.streamlit.app/) - Análises completas
- [🎨 Construtor Visual](https://circuitos-rlc-construtor.streamlit.app/) - Editor de circuitos

---

## ⭐ **CARACTERÍSTICAS ESPECIAIS**

### **Interface Amigável:**
- 🎨 Design moderno e intuitivo
- 📱 Responsivo para todos os dispositivos
- 🌈 Gráficos interativos coloridos
- ⚡ Atualização em tempo real

### **Educacionalmente Focado:**
- 📖 Explicações claras dos resultados
- 🧮 Fórmulas mostradas junto com cálculos
- 📊 Múltiplas visualizações do mesmo conceito
- 🎯 Presets para casos comuns de estudo

---

**🎓 Desenvolvido para facilitar o aprendizado de circuitos elétricos**  
**⚡ Transformando conceitos abstratos em experiências visuais e interativas**

---

### 🆘 **Suporte**
Dúvidas ou problemas? Entre em contato através do repositório GitHub ou com seu professor.
