import importlib.util
from pathlib import Path

from generated_protocol import SensorReading


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


def test_sensor_history_roundtrip():
    original = SensorReading(
        sensor_id="S-001",
        location="Greenhouse-A",
        temperature_c=23.7,
        humidity_pct=61.2,
        timestamp=123,
        battery_pct=82,
        history=[23.5, 23.6, 23.7],
    )

    payload = original.serialize()
    restored, offset = SensorReading.deserialize_from(payload)

    assert len(restored.history) == 3
    assert abs(restored.history[0] - 23.5) < 0.001
    assert abs(restored.history[1] - 23.6) < 0.001
    assert abs(restored.history[2] - 23.7) < 0.001
    assert offset == len(payload)
