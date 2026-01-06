from gem_workflow.cli.output_discipline import beta_output_has_single_final_json


def test_beta_output_requires_single_final_json_block():
    valid = """
BETA_MODE: AUDIT
Some content.
```json
{"handoff_version": "1.4.1"}
```
"""
    assert beta_output_has_single_final_json(valid) is True


def test_beta_output_rejects_multiple_json_blocks():
    invalid = """
```json
{"one": 1}
```
```json
{"two": 2}
```
"""
    assert beta_output_has_single_final_json(invalid) is False


def test_beta_output_rejects_non_terminal_json():
    invalid = """
```json
{"handoff_version": "1.4.1"}
```
Trailing text
"""
    assert beta_output_has_single_final_json(invalid) is False
