# 🌲 Helldivers: Visualizador de Árvores Binárias

> **"Pela Democracia Gerenciada! Pelo Aprendizado de Algoritmos!"**

Um visualizador interativo e gamificado de Estruturas de Dados Avançadas, desenvolvido em Python com Pygame. O projeto permite a visualização passo-a-passo de operações complexas (inserção, busca, remoção e balanceamento) com uma interface temática inspirada no universo de *Helldivers*.

---


## 🚀 Funcionalidades

* **6 Tipos de Estruturas:** Do básico ao avançado, incluindo visualização espacial.
* **Animação Passo-a-Passo:** Diferente de outros visualizadores, este mostra o "raciocínio" do algoritmo (ex: descendo pelos nós, colorindo caminhos, rotacionando).
* **Fila de Processamento:** Visualize quais dados serão inseridos na sequência.
* **Modo Turbo (Fast Fill):** Preencha a árvore com centenas de nós em instantes.
* **Visualização Espacial (KD-Tree):** Veja como algoritmos de árvore particionam um plano 2D.
* **Arquitetura Modular:** Código organizado utilizando padrões de projeto e separação de responsabilidades.

### Estruturas Suportadas:
1.  **Árvore Rubro-Negra (Red-Black):** Balanceamento por regras de cores.
2.  **Árvore 2-3-4 (B-Tree):** Árvore multi-way (nós com múltiplas chaves).
---

## 🎮 Controles e Comandos

A interação é feita via teclado e mouse. O sistema possui um **Log de Eventos** na tela para explicar cada operação.

### Navegação
| Tecla | Ação |
| :---: | :--- |
| `1` a `2` | **Trocar de Fase** (Muda o tipo de árvore) |
| `T` | **Tutorial** (Exibe a ajuda da fase atual) |
| `ESC` | **Sair** do programa |

### Manipulação de Dados
| Tecla | Nome | Descrição |
| :---: | :--- | :--- |
| `I` | **Inserir** | Insere o próximo item da fila (destacado) ou um aleatório. |
| `X` | **Remover** | Remove o nó atualmente selecionado (clique para selecionar). |
| `B` | **Buscar** | Realiza uma busca animada pelo nó selecionado. |
| `M` | **Misturar** | Randomiza e gera novos valores para a fila de inserção. |
| `R` | **Reset** | Limpa a árvore e restaura a fila inicial. |

### Automação
| Tecla | Nome | Descrição |
| :---: | :--- | :--- |
| `A` | **Auto (Lento)** | Inicia a inserção automática passo-a-passo (ideal para estudar). |
| `F` | **Fill (Turbo)** | Preenche a árvore instantaneamente com a fila restante. |
| `Espaço`| **Pause** | Pausa qualquer operação automática em andamento. |

---

## 📚 Detalhes das Fases

### 1. Árvore Rubro-Negra
Foca no balanceamento por cores e propriedades.
* **Observe:** A recolorização de nós (Tio Vermelho) vs Rotações (Tio Preto).

### 2. Árvore 2-3-4
Uma introdução às árvores B (usadas em bancos de dados).
* **Observe:** O processo de "Split" (divisão), onde um nó cheio empurra a chave mediana para o pai.

---

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/augustorodrigues-dev/arvores-binarias-em-python
    cd arvores-binarias-em-python
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o projeto:**
    ```bash
    python main.py
    ```

---

## 🏗️ Arquitetura do Código

O projeto foi refatorado para garantir manutenibilidade e separação de conceitos:

* **`main.py`**: Ponto de entrada. Apenas inicializa a aplicação.
* **`game.py`**: O "coração" do jogo. Gerencia o loop principal, eventos de entrada (teclado/mouse) e estados.
* **`ui.py`**: Responsável por desenhar textos, HUD, tutoriais e menus.
* **`layout.py`**: Contém a matemática pura para calcular as coordenadas (X, Y) dos nós na tela.
* **`gerenciamento.py`** (TreeManager): Design Pattern *Facade*. Gerencia a troca dinâmica entre os tipos de árvores.
* **`config.py`**: Constantes globais (Cores, Resolução, Listas de Dados).
* **Implementações das Árvores:**
    * `rb.py`, `t234.py`.

---