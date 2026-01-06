import re

JSON_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def extract_json_blocks(text: str) -> list[str]:
    return [match.group(1).strip() for match in JSON_BLOCK_PATTERN.finditer(text)]


def beta_output_has_single_final_json(text: str) -> bool:
    blocks = extract_json_blocks(text)
    if len(blocks) != 1:
        return False
    stripped = text.strip()
    last_block = f"```json\n{blocks[0]}\n```"
    return stripped.endswith(last_block)
