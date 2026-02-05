import yaml
from pathlib import Path
import sys

OUTPUT_FULL = "extracted_full.yaml"
OUTPUT_PROMPT_GOAL = "extracted_prompt_goal.yaml"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_tests(data):
    extracted_full = []
    extracted_prompt_goal = []

    tests = data.get("tests", [])

    for test in tests:
        prompt = test.get("vars", {}).get("prompt")

        # Extract metric from first assert entry (if present)
        metric = None
        asserts = test.get("assert", [])
        if isinstance(asserts, list) and asserts:
            metric = asserts[0].get("metric")

        metadata = test.get("metadata", {})
        plugin_id = metadata.get("pluginId")
        goal = metadata.get("goal")

        if prompt and goal:
            extracted_full.append({
                "prompt": prompt,
                "metric": metric,
                "pluginId": plugin_id,
                "goal": goal
            })

            extracted_prompt_goal.append({
                "prompt": prompt,
                "goal": goal
            })

    return extracted_full, extracted_prompt_goal


def write_yaml(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def main():
    input_path = input("Enter path to the input YAML file: ").strip()
    input_file = Path(input_path)

    if not input_file.exists() or not input_file.is_file():
        print(f"Error: File not found -> {input_file}")
        sys.exit(1)

    try:
        data = load_yaml(input_file)
    except Exception as e:
        print(f"Failed to read YAML file: {e}")
        sys.exit(1)

    extracted_full, extracted_prompt_goal = extract_tests(data)

    write_yaml(Path(OUTPUT_FULL), extracted_full)
    write_yaml(Path(OUTPUT_PROMPT_GOAL), extracted_prompt_goal)

    print(f"Created '{OUTPUT_FULL}' with {len(extracted_full)} entries")
    print(f"Created '{OUTPUT_PROMPT_GOAL}' with {len(extracted_prompt_goal)} entries")


if __name__ == "__main__":
    main()
