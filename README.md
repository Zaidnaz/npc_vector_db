# 🛡️ NPC Personality Engine (with Memory)

A Python-based AI NPC ("Garrett the Grumpy Blacksmith") that **remembers your past interactions** using a Vector Database.

## 🚀 How it Works
* **Brain:** Local LLM via **Ollama** (Llama 3 or Mistral).
* **Memory:** Vector storage via **ChromaDB**.
* **Logic:** Retrieves past chat history to influence the NPC's current attitude (e.g., if you helped him yesterday, he trusts you today).

## 🛠️ Prerequisites
1.  [Python 3.10+](https://www.python.org/downloads/)
2.  [Ollama](https://ollama.com/) installed and running.

## 📥 Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/yourusername/npc-memory-engine.git](https://github.com/yourusername/npc-memory-engine.git)
    cd npc-memory-engine
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install chromadb ollama
    ```

3.  **Download the AI Model:**
    Open your terminal and run:
    ```bash
    ollama pull llama3.2:3b
    ```
    *(Note: If you use a different model, update `MODEL_NAME` in `npc_engine.py`)*.

## 🎮 Usage

1.  Make sure Ollama is ready (it runs in the background usually).
2.  Run the script:
    ```bash
    python npc_engine.py
    ```
3.  Chat with Garrett! Type `exit` to save and quit.

## 🧠 Memory Persistence
The project creates a local folder `npc_memory_db/` to store memories.
* **To reset memory:** Delete the `npc_memory_db/` folder.
* **Git:** This folder is ignored by `.gitignore` to keep your repo clean.