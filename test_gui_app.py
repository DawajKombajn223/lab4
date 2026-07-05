from gui_app import build_sample_reading, format_log_entry


def test_build_sample_reading():
    reading = build_sample_reading()
    assert reading.sensor_id == "S-001"
    assert reading.location == "Greenhouse-A"
    assert reading.temperature_c > 0


def test_format_log_entry_contains_status():
    line = format_log_entry("received", "Pomiar odebrany")
    assert "received" in line
    assert "Pomiar odebrany" in line
