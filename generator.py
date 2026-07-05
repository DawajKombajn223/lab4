import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def main() -> None:
    root = Path(__file__).parent
    schema_path = root / "interface.json"
    template_dir = root / "templates"
    output_path = root / "generated_protocol.py"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("protocol.py.j2")

    rendered = template.render(structs=schema["structs"], types=schema["types"])
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wygenerowano: {output_path}")


if __name__ == "__main__":
    main()
