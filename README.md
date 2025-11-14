
#  Circuit Analyzer Pro

### **Análise Avançada de Circuitos RLC – Interativo, Educacional e Completo**

O **Circuit Analyzer Pro** é uma ferramenta gráfica desenvolvida em **Python + Tkinter + Matplotlib** para análise completa de **circuitos elétricos RLC**, em regime permanente, transitório e em frequência.
O software também inclui um **designer de circuitos**, geração de diagramas fasoriais, cálculos automáticos, gráficos interativos e relatórios detalhados.

---

## 🧠 **Objetivo do Projeto**

Este programa foi criado para auxiliar estudantes de Engenharia a compreender, visualizar e analisar:

✔ Circuitos RLC série e paralelo
✔ Resposta em regime permanente
✔ Resposta transitória (degrau, impulso e natural)
✔ Resposta em frequência
✔ Cálculo automático de impedância, potências e fasores
✔ Correção do fator de potência
✔ Representações gráficas completas

É uma ferramenta voltada para **aprendizado**, **experimentação**, **visualização** e **demonstração em sala de aula**.

---

# 📸 Interface do Sistema

O software possui quatro áreas principais:

### **1️⃣ Barra lateral – Painel de Controle**

Aqui o usuário define os parâmetros do circuito:

* Frequência
* Tensão e corrente
* Ângulos fasoriais
* Valores de R, L e C
* Botões rápidos (impedância, ressonância, correção FP)

---

### **2️⃣ Aba – Sinais Elétricos**

Gera automaticamente:

* Gráfico de **tensão v(t)**
* Gráfico de **corrente i(t)**
* Gráfico de **potência instantânea p(t)**
* Marcações de **defasagem entre sinais**

---

### **3️⃣ Aba – Diagrama Fasorial**

Mostra 4 gráficos simultâneos:

* Fasores de tensão e corrente
* Fasor da impedância (R + jX)
* Triângulo de potência (P, Q e S)
* Representação de números complexos

Tudo em gráfico polar interativo.

---

### **4️⃣ Aba – Designer de Circuitos**

Permite escolher:

* 🔗 RLC em Série
* ⚡ RLC em Paralelo
* 🔄 DC por Malhas

Além disso, desenha automaticamente o circuito com:

* Resistor detalhado
* Indutor com bobinas
* Capacitor estilizado
* Fonte de tensão
* Setas de corrente
* Conexões elétricas
* Título automático com valores reais

---

### **5️⃣ Aba – Relatórios Automáticos**

Aqui aparecem textos gerados automaticamente com:

* Cálculos passo-a-passo
* Explicação das fórmulas
* Impedância complexa
* Potências e fator de potência
* Ressonância
* Resultados da análise transitória
* Resultados da análise de frequência

Excelente para usar na apresentação ou exportar para trabalho.

---

# 🧮 **Funcionalidades Principais**

## 🔸 1. **Análise de Regime Permanente (Fasores)**

* Converte tensões e correntes para RMS
* Cria fasores complexos
* Calcula impedância:
  [
  Z = \frac{V}{I}
  ]
* Separa parte real (R) e imaginária (X)
* Calcula potência ativa P, reativa Q e aparente S

---

## 🔸 2. **Cálculo de Impedância**

Para RLC Série:
[
Z = R + j(\omega L - \frac{1}{\omega C})
]

Para RLC Paralelo:
[
Y = Y_R + Y_L + Y_C
\quad\Rightarrow\quad Z = \frac{1}{Y}
]

---

## 🔸 3. **Frequência de Ressonância**

[
f_0 = \frac{1}{2\pi\sqrt{LC}}
]

A ferramenta calcula automaticamente:

* XL
* XC
* Verificação XL = XC
* Impedância mínima
* Corrente máxima

---

## 🔸 4. **Correção do Fator de Potência**

O software calcula automaticamente o capacitor necessário para corrigir o FP:

[
Q_C = Q_1 - Q_2
]

[
C = \frac{Q_C}{V^2 \cdot 2\pi f}
]

---

## 🔸 5. **Análise Transitória (Degrau, Impulso e Natural)**

Para circuito RLC série:

* Sistema subamortecido (ζ < 1)
* Criticamente amortecido (ζ = 1)
* Superamortecido (ζ > 1)

O software calcula:

[
\omega_n = \frac{1}{\sqrt{LC}}
\qquad
\zeta = \frac{R}{2}\sqrt{\frac{C}{L}}
]

E gera automaticamente:

* vC(t)
* iL(t)

Com destaque para:

* Tempo de subida
* Amortecimento
* Vibração
* Regime final

---

## 🔸 6. **Análise em Frequência (Bode, Nyquist, Magnitude/Fase)**

Cálculo via função de transferência:

[
H(j\omega) = \frac{1}{1 + j\omega RC + (j\omega)^2 LC}
]

O sistema gera:

* Diagrama de Bode (magnitude e fase)
* Diagrama de Nyquist
* Magnitude × frequência
* Fase × frequência

---

# 🖥️ Como Executar

### **1. Instale as dependências**

```bash
pip install numpy matplotlib
```

(Tkinter já vem com o Python em Windows e Linux.)

### **2. Execute o programa**

```bash
python app.py
```

---

# 📚 O que posso demonstrar na apresentação?

Aqui vai um roteiro pronto para usar em sala:

### ** 1 — Apresentação do Software**

* Nome: Circuit Analyzer Pro
* Objetivo: facilitar o estudo de circuitos RLC
* Tecnologias: Python, Tkinter, Matplotlib

### ** 2 — Interface**

* Explicar barra lateral
* Explicar abas
* Mostrar interatividade

### ** 3 — Teoria**

* Impedância
* Fasores
* Potências
* Ressonância

### ** 4 — Demonstração ao vivo**

* Inserir valores
* Gerar sinais
* Abrir fasores
* Alterar R, L, C
* Plotar ressonância

### ** 5 — Análise Transitória**

* Mostrar diferença entre ζ < 1, = 1 e > 1

### ** 6 — Conclusão**

* Ferramenta educacional
* Visual e intuitiva
* Auxilia no entendimento de sistemas elétricos

---

# 📄 Licença

Uso educacional e demonstrativo.
