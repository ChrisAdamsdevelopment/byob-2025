import random, string, re

def generate_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def insert_junk(code):
    junk = f"\nfor _ in range({random.randint(1, 3)}):\n    pass  # junk loop\n"
    return junk + code + junk

def mutate_identifiers(code):
    reserved = {'def', 'class', 'import', 'return', 'if', 'else', 'for', 'while'}
    identifiers = set(re.findall(r'\b[_a-zA-Z][_a-zA-Z0-9]{2,}\b', code))
    replacements = {id: generate_name() for id in identifiers if id not in reserved}
    for old, new in replacements.items():
        code = re.sub(rf'\b{old}\b', new, code)
    return code

def mutate_code(code):
    code = mutate_identifiers(code)
    code = insert_junk(code)
    return code
