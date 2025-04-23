# 🐦 PULA PULA

Um jogo estilo *Flappy Bird* desenvolvido com Python, OpenGL e GLFW. O objetivo é desviar de obstáculos e sobreviver o maior tempo possível. Inclui inimigos voadores, escurecimento progressivo do fundo e som ambiente.

---

## 📁 Estrutura do Projeto

```
PULA_PULA/
├── assets/
│   ├── background.png
│   └── bird.png
├── img/
│   ├── bird/
│   │   ├── b0.png
│   │   ├── b1.png
│   │   ├── b2.png
│   │   └── b0.png
│   ├── ground/
│   │   ├── g0.png
│   │   └── g1.png
│   ├── tap/
│   │   ├── t0.png
│   │   └── t1.png
│   ├── BG.png
│   ├── botpipe.png
│   ├── getready.png
│   ├── go.png
│   ├── ground.png
│   └── toppipe.png
├── sfx/
│   ├── die.wav
│   ├── flap.wav
│   ├── hit.wav
│   ├── score.wav
│   └── start.wav
├── venv39/
├── .gitignore
├── README.md
├── requirements.txt
├── background.py
├── bird.py
├── enemy_bird.py
├── game_engine.py
├── game_over_screen.py
├── game.py
├── get_ready_screen.py
├── ground.py
├── pipe.py
├── renderer.py
├── score.py
└── texture.py
```

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/daniel-santos92/pula_pula.git
cd pula_pula
```

### 2. (Opcional) Crie e ative um ambiente virtual

```bash
python -m venv venv39
.env39\Scriptsctivate  # Windows
# source venv39/bin/activate  # Linux/macOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o jogo

```bash
python game.py
```

---

## 🛠 Tecnologias Utilizadas

- Python 3.x
- PyOpenGL
- GLFW
- Pygame
- Estrutura modular em Programação Orientada a Objetos (POO)

---

---

## 🎮 Créditos

Desenvolvido por [Daniel Santos](https://github.com/daniel-santos92), [Victor](https://github.com/victorpazs), [Lucas](https://github.com/LKTeloeken), [Vinícius](https://github.com/2viny) como projeto de aprendizado e experimentação com jogos 2D em Python.