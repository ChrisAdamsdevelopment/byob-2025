import re, random, string

def randomize_identifiers(code):
    identifiers = set(re.findall(r'\b[_a-zA-Z][_a-zA-Z0-9]{2,}\b', code))
    translation = {id: ''.join(random.choices(string.ascii_letters, k=10)) for id in identifiers if id not in ['def', 'class', 'import', 'return', 'print']}
    for old, new in translation.items():
        code = code.replace(old, new)
    return code

def obfuscate_code(code):
    code = randomize_identifiers(code)
    return code
