# Árvores em Python

> **"Pela Democracia Gerenciada! Pelo Aprendizado!"**

Um visualizador interativo de Estruturas de Dados Avançadas (Árvores) desenvolvido em Python com Pygame. Este projeto gamifica o estudo de algoritmos, permitindo a inserção, remoção e busca visual em diferentes tipos de árvores, com uma temática inspirada no universo de Helldivers.

## Sobre o Projeto

Este software foi criado para auxiliar no entendimento visual de como estruturas de dados complexas funcionam internamente. O projeto é modular e implementa quatro tipos principais de árvores, divididas em 5 fases de visualização.

### Estruturas Suportadas:
1.  **Árvore AVL:** Árvore binária de busca balanceada por altura.
2.  **Árvore Rubro-Negra (Red-Black):** Balanceamento baseado em cores (regras de nós vermelhos/pretos).
3.  **Árvore 2-3-4:** Árvore B de ordem 4 (multi-way), onde nós podem ter mais de uma chave.
4.  **KD-Tree (k-Dimensional):** Estrutura para particionamento de espaço (focada aqui em 2D).

---

## Funcionalidades

* **Visualização em Tempo Real:** Veja nós sendo criados, arestas conectadas e cores alteradas instantaneamente.
* **Interatividade:** Insira valores aleatórios, clique para selecionar nós e realize buscas visuais.
* **Modo KD-Tree Duplo:**
    * **Visão Hierárquica:** Veja a estrutura lógica da árvore (pai/filho).
    * **Visão Espacial (Plano 2D):** Veja como os cortes dividem o espaço cartesiano.
* **Persistência de Dados (KD-Tree):** Alterne entre a visão hierárquica e espacial sem perder os dados inseridos.
* **Dados Automáticos:** Na visão espacial, as coordenadas (X, Y) são exibidas automaticamente sobre os pontos.

---

## Instalação e Execução

### Passo a Passo

1.  **Clone o repositório** (ou baixe os arquivos):
    ```bash
    git clone https://github.com/augustorodrigues-dev/arvores-binarias-em-python
    cd arvores-binarias-em-python
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o projeto:**
    Certifique-se de que todos os arquivos (`main.py`, `ui.py`, `config.py`, `fachada.py`, etc.) estão na mesma pasta.
    ```bash
    python main.py
    ```

---

## Controles e Fases

Use o teclado e o mouse para controlar a simulação.

### Teclas Globais
| Tecla | Ação |
| :--- | :--- |
| `1` a `5` | Troca de Fase (Muda o tipo de árvore) |
| `T` | Abre/Fecha o Tutorial da fase atual |
| `ESC` | Encerra o programa |
| `Clique` | Seleciona um nó para ver detalhes ou remover |

### Ações de Dados
| Tecla | Ação | Descrição |
| :--- | :--- | :--- |
| `M` | **Misturar** | Aleatoriza os vértices a serem inseridos |
| `I` | **Inserir** | Adiciona um valor (ou ponto X,Y) aleatório. |
| `A` | **Auto Inserção** | Insere passo a passo os vértices na árvore. |
| `F` | **Preencher** | Preenche toda a árvore rapidamente. |
| `B` | **Buscar** | Realiza a busca visual do vértice selecionado. |
| `X` | **Remover** | Remove o nó selecionado. |
| `R` | **Reset** | Reseta a árvore. |
| `ESPAÇO` | **Stop** | Pausa a execução. |

---

## Detalhes das Fases

### Fase 1: Árvore AVL
Foca no balanceamento rigoroso. Observe como a árvore rotaciona para manter a diferença de altura entre subárvores no máximo em 1.
* *Destaque:* Única fase que suporta remoção com rebalanceamento visual.

### Fase 2: Árvore Rubro-Negra
Foca no balanceamento por cores.
* *Regras:* Raiz sempre preta, nós vermelhos não têm filhos vermelhos.

### Fase 3: Árvore 2-3-4
Visualização de nós retangulares que podem conter até 3 chaves.
* *Mecânica:* Observe o "split" (divisão) de nós quando eles ficam cheios e a árvore cresce para cima.

### Fase 4: KD-Tree (Hierarquia)
Mostra a estrutura lógica da KD-Tree.
* *Cores:* Nós pares (Vermelhos) cortam o eixo X, nós ímpares (Azuis) cortam o eixo Y.

### Fase 5: KD-Tree (Plano 2D)
A mesma árvore da Fase 4, mas visualizada geometricamente.
* *Visual:* Veja os pontos plotados no espaço e as linhas de corte dividindo a tela. Os valores (X, Y) são exibidos automaticamente para facilitar a leitura.

---

## Estrutura do Código

O projeto foi refatorado seguindo princípios de modularidade:

* **`main.py`**: Loop principal, gerenciamento de estados e tratamento de eventos.
* **`ui.py`**: Gerencia toda a interface gráfica, textos, HUD e tutoriais.
* **`fachada.py`**: Design Pattern *Facade*. Unifica a comunicação com as árvores.
* **`config.py`**: Arquivo central de configurações (cores, dimensões).
* **`avl.py`**: Lógica da Árvore AVL.
* **`rb.py`**: Lógica da Árvore Rubro-Negra.
* **`t234.py`**: Lógica da Árvore 2-3-4.
* **`kdtree.py`**: Lógica da KD-Tree.

---
