import ollama
import chromadb
import uuid
from datetime import datetime

# --- CONFIGURATION ---
NPC_NAME = "Garrett"
NPC_ROLE = "A grumpy, cynical blacksmith in a medieval fantasy village. He hates adventurers because they always break his tools."
MODEL_NAME = "llama3.2:3b" # or "mistral", whatever you have installed

# --- SETUP VECTOR DATABASE ---
# This creates a local folder 'npc_memory_db' to store data persistently
client = chromadb.PersistentClient(path="./npc_memory_db")

# Create (or get) a collection. This is like a table in SQL.
# Chroma uses a default embedding model (all-MiniLM-L6-v2) automatically!
memory_collection = client.get_or_create_collection(name="npc_memories")

def add_memory(user_text, npc_response):
    """
    Saves the interaction to the Vector DB.
    We store the text, and Chroma automatically turns it into a vector.
    """
    interaction = f"User said: '{user_text}' | {NPC_NAME} replied: '{npc_response}'"
    
    memory_collection.add(
        documents=[interaction],
        metadatas=[{"timestamp": str(datetime.now())}],
        ids=[str(uuid.uuid4())] # Unique ID for each memory
    )
    print(f"   [System] Memory stored.")

def retrieve_memories(query_text, n_results=2):
    """
    The Vector Search Magic.
    It looks for memories SIMILAR to what the user just said.
    """
    results = memory_collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Extract the documents from the result structure
    memories = results['documents'][0]
    return memories

def chat_with_npc():
    print(f"--- Entering the Smithy. You see {NPC_NAME}. ---")
    print("(Type 'exit' to leave)")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # 1. SEARCH MEMORY: Has the user talked about this topic before?
        past_memories = retrieve_memories(user_input)
        
        # Format memories for the prompt
        memory_context = ""
        if past_memories:
            memory_context = "RELEVANT PAST HISTORY:\n" + "\n".join(f"- {m}" for m in past_memories)
        
        # 2. CONSTRUCT PROMPT
        # We give the LLM the Persona + The Retrieved Memories + Current Input
        system_prompt = f"""
        You are roleplaying as {NPC_NAME}. {NPC_ROLE}
        
        {memory_context}
        
        Use the past history to inform your attitude. If the user was rude before, stay angry. If they were helpful, be slightly nicer.
        Keep responses short (under 2 sentences) and conversational.
        """

        # 3. GENERATE RESPONSE (Ollama)
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input},
        ])
        
        npc_reply = response['message']['content']
        print(f"{NPC_NAME}: {npc_reply}")

        # 4. SAVE NEW MEMORY
        add_memory(user_input, npc_reply)

if __name__ == "__main__":
    chat_with_npc()