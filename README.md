# 🔐 DES — Cifragem de Arquivos Binários

Implementação do algoritmo **DES (Data Encryption Standard)** do zero, em Python puro, sem uso de bibliotecas de criptografia externas. Suporta arquivos binários (`.jpg`, `.png`, `.pdf`, etc.) com padding **PKCS#7**.

---

## 📖 Fundamentação Teórica

### O que é DES?

O DES (Data Encryption Standard) é um algoritmo de **cifra de bloco simétrico**, padronizado pelo NIST em 1977. Ele opera sobre blocos de **64 bits (8 bytes)** e utiliza uma chave de **64 bits**, da qual 56 bits são efetivamente usados na criptografia (os outros 8 são bits de paridade).

Apesar de considerado obsoleto para uso em produção (por conta do tamanho pequeno da chave), o DES é amplamente estudado por ser a base conceitual do **3DES** e do moderno **AES**.

---

### Estrutura da Rede de Feistel

O DES utiliza uma **Rede de Feistel** com **16 rodadas**. Em cada rodada:

1. O bloco de 64 bits é dividido em duas metades: **L** (esquerda) e **R** (direita)
2. A metade direita passa pela **função F** junto com a subchave da rodada
3. O resultado é submetido a XOR com a metade esquerda
4. As metades são trocadas para a próxima rodada

```
L[i+1] = R[i]
R[i+1] = L[i] XOR F(R[i], K[i])
```

A elegância da Rede de Feistel é que **a decifragem usa exatamente a mesma estrutura**, apenas com as subchaves em ordem inversa.

---

### Função F

A função F é o núcleo do DES e possui 4 etapas:

| Etapa | Descrição | Bits |
|---|---|---|
| **Expansão (E)** | Expande R de 32 para 48 bits | 32 → 48 |
| **XOR** | XOR com a subchave da rodada | 48 → 48 |
| **S-Boxes** | 8 caixas de substituição não-lineares | 48 → 32 |
| **Permutação (P)** | Embaralha os 32 bits resultantes | 32 → 32 |

As **S-Boxes** são o elemento de segurança mais importante do DES — são tabelas de substituição não-lineares que dificultam a análise criptográfica.

---

### Key Schedule (Geração de Subchaves)

A partir da chave de 64 bits, o DES gera **16 subchaves de 48 bits**:

1. Aplica **PC-1**: reduz a chave de 64 para 56 bits
2. Divide em duas metades **C** e **D** de 28 bits
3. Para cada rodada: aplica rotação circular para a esquerda (1 ou 2 posições)
4. Aplica **PC-2**: comprime C+D de 56 para 48 bits → subchave da rodada

---

### Padding PKCS#7

Arquivos raramente têm tamanho múltiplo de 8 bytes. O **PKCS#7** resolve isso:

- Calcula quantos bytes faltam para completar o último bloco (`n`)
- Preenche com `n` bytes, todos com o valor `n`

**Exemplo:** arquivo com 13 bytes → faltam 3 bytes → adiciona `03 03 03`

Na decifragem, basta ler o último byte para saber quantos bytes de padding remover.

---

## 🛠️ Requisitos

- **Python 3.6+** (sem dependências externas)

Verifique sua versão:
```bash
python --version
```

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/implementacaodes-criptografia.git
cd implementacaodes-criptografia
```

### 2. Execute o programa

```bash
python des_cipher.py
```

### 3. Cifrar um arquivo

```
[1] Cifrar arquivo
Caminho do arquivo de entrada: foto.jpg
Caminho do arquivo cifrado (saída): foto.enc
Chave (qualquer texto, até 8 chars): minhaKey
```

### 4. Decifrar um arquivo

```
[2] Decifrar arquivo
Caminho do arquivo cifrado: foto.enc
Caminho do arquivo decifrado (saída): foto_decifrada.jpg
Chave usada na cifragem: minhaKey
```

---

## 📌 Observações

- A chave pode ser qualquer texto de **até 8 caracteres**. Se menor que 8, é preenchida com zeros automaticamente.
- O arquivo decifrado com a chave correta será **idêntico ao original**.
- Usar uma chave errada na decifragem resultará em erro de padding ou arquivo corrompido.

---

## 📁 Estrutura do Projeto

```
implementacaodes-criptografia/
├── des_cipher.py   # Implementação completa do DES
└── README.md       # Este arquivo
```

---

## 👨‍💻 Autor

Desenvolvido por **Arthur Xavier** 
