conversation_memory = {}

def get_memory(user_email):
    if user_email not in conversation_memory:
        conversation_memory[user_email] = []

    return conversation_memory[user_email]


def add_memory(user_email, role, content):
    memory = get_memory(user_email)

    memory.append({
        "role": role,
        "content": content
    })

    # keep only last 6 messages
    conversation_memory[user_email] = memory[-6:]


def format_memory(user_email):
    memory = get_memory(user_email)

    if not memory:
        return "No previous conversation."

    text = ""

    for m in memory:
        text += f"{m['role'].title()}: {m['content']}\n"

    return text
