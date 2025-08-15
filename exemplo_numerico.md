# 📊 Exemplo Numérico Simples - Sistema de Roteamento Logístico

## 🏢 Cenário da Empresa

**Empresa**: LogiTech Express
**Horário de Operação**: 8 horas (480 minutos)
**Frota**: 3 veículos
**Centros de Distribuição**: 4 localizações

## 🗺️ Mapa da Rede Logística

```
        [A] Centro Principal
         |  (Capacidade: 1000 unidades)
         |  (Tempo carga/descarga: 30 min)
         |
    [B]--+--[C]
    |     |     |
    |     |     |
   [D]   [E]   [F]
```

### **Localizações e Capacidades**
- **A (Centro Principal)**: Capacidade 1000, Tempo carga/descarga: 30 min
- **B (Depósito Norte)**: Capacidade 500, Tempo carga/descarga: 20 min  
- **C (Depósito Sul)**: Capacidade 500, Tempo carga/descarga: 20 min
- **D (Cliente Norte)**: Capacidade 200, Tempo carga/descarga: 15 min
- **E (Cliente Centro)**: Capacidade 200, Tempo carga/descarga: 15 min
- **F (Cliente Sul)**: Capacidade 200, Tempo carga/descarga: 15 min

### **Tempos de Trânsito (minutos)**
```
    A   B   C   D   E   F
A   0   20  25  35  30  40
B  20   0   15  15  25  35
C  25  15   0   35  25  15
D  35  15  35   0   20  30
E  30  25  25  20   0   20
F  40  35  15  30  20   0
```

## 🚚 Frota de Veículos

| Veículo | Capacidade | Localização Inicial | Velocidade |
|----------|------------|---------------------|------------|
| V1       | 300        | A                   | 1 unidade/min |
| V2       | 250        | A                   | 1 unidade/min |
| V3       | 200        | A                   | 1 unidade/min |

## 📦 Pedidos Pendentes

| Pedido | Origem | Destino | Quantidade | Prazo (min) | Prioridade |
|--------|--------|---------|------------|-------------|------------|
| P1     | A      | D       | 150        | 120         | Alta       |
| P2     | A      | E       | 100        | 180         | Média      |
| P3     | A      | F       | 200        | 240         | Baixa      |
| P4     | B      | D       | 80         | 90          | Alta       |
| P5     | C      | F       | 120        | 150         | Média      |
| P6     | A      | B       | 200        | 300         | Baixa      |

## ⏱️ Simulação Temporal

### **Minuto 0-30: Carregamento Inicial**
- V1, V2, V3 carregam em A
- V1: 150 unidades (P1)
- V2: 100 unidades (P2) 
- V3: 200 unidades (P3)

### **Minuto 30-65: Primeira Rota**
- V1: A → D (35 min) → Entrega P1 (15 min) = **50 min total**
- V2: A → E (30 min) → Entrega P2 (15 min) = **45 min total**
- V3: A → F (40 min) → Entrega P3 (15 min) = **55 min total**

### **Minuto 65-100: Retorno e Nova Carga**
- V1: D → A (35 min) = **100 min total**
- V2: E → A (30 min) = **75 min total**
- V3: F → A (40 min) = **95 min total**

## 📊 Métricas de Performance

### **Sistema Atual (Política Aleatória)**
- **Taxa de Entrega no Prazo**: 4/6 = **66.7%**
- **Tempo Médio de Atraso**: 45 minutos
- **Eficiência da Frota**: 1.2 (baixa)
- **Utilização de Capacidade**: 65%

### **Sistema Otimizado (Meta)**
- **Taxa de Entrega no Prazo**: 6/6 = **100%**
- **Tempo Médio de Atraso**: 0 minutos
- **Eficiência da Frota**: 2.8 (alta)
- **Utilização de Capacidade**: 85%

## 🎯 Problemas Identificados

1. **V1** faz rota A→D→A (70 min) quando poderia fazer A→D→B→A (70 min) e pegar P4
2. **V2** retorna vazio de E quando poderia ir para C pegar P5
3. **V3** não aproveita capacidade total (200 vs 150 necessários para P1)

## 💡 Oportunidades de Otimização

1. **Rota Combinada**: V1: A→D→B→A (pegar P1 + P4)
2. **Rota Eficiente**: V2: A→E→C→F→A (pegar P2 + P5 + P3)
3. **Balanceamento**: V3: A→B (pegar P6) enquanto outros fazem entregas

## 🔢 Cálculo de Benefícios

### **Tempo Economizado**
- Sistema atual: 480 min para 6 pedidos
- Sistema otimizado: 320 min para 6 pedidos
- **Economia**: 160 minutos (33.3%)

### **Capacidade Aproveitada**
- Sistema atual: 650/750 = 86.7%
- Sistema otimizado: 750/750 = 100%
- **Melhoria**: 13.3%

### **Custo Operacional**
- Sistema atual: 3 veículos × 480 min = 1440 min-veículo
- Sistema otimizado: 3 veículos × 320 min = 960 min-veículo
- **Redução**: 33.3%

---

*Este exemplo demonstra como pequenas otimizações podem gerar grandes impactos em sistemas logísticos reais.* 