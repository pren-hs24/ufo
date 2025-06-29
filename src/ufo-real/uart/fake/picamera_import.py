# uart/fake/picamera_import.py

def setup_picamera_import():
    import sys
    import types
    import platform

    if platform.system() == "Linux":
        try:
            from picamera2 import picamera2 # type: ignore
        except ImportError:
            print("[WARNING] Picamera2 not installed!")
    else:
        class FakePicamera2:
            def __init__(self, *args, **kwargs):
                print("[WARNUNG] Fake-Picamera2 aktiv – keine echte Kamera.")

            def start(self):
                print("[Fake] start()")

            def stop(self):
                print("[Fake] stop()")

            def capture(self):
                print("[Fake] capture()")
                return b"FakeBild"

        # RICHTIGES "Modul" bauen
        fake_module = types.ModuleType("picamera2")
        fake_module.Picamera2 = FakePicamera2 # type: ignore

        # In sys.modules registrieren
        sys.modules["picamera2"] = fake_module
