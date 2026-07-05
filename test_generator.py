import importlib.util
from pathlib import Path


def test_generator_creates_output_file():
    generator_path = Path("generator.py")
    assert generator_path.exists(), "generator.py should exist"

    spec = importlib.util.spec_from_file_location("generator", generator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    module.main()

    output_path = Path("generated_protocol.py")
    assert output_path.exists(), "generated_protocol.py should be created"
    content = output_path.read_text(encoding="utf-8")
    assert "class SensorReading" in content
    assert "class ReceiverAck" in content
