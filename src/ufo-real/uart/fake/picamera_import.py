# uart/fake/picamera_import.py

# -*- coding: utf-8 -*-
"""Fake Picamera Import for testing"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import platform
import sys
import types


def setup_picamera_import():
    """fake a picamera import"""

    if platform.system() == "Linux":
        try:
            from picamera2 import picamera2  # type: ignore
        except ImportError:
            print("[WARNING] Picamera2 not installed!")
    else:

        class FakePicamera2:
            """Fake Camera Class"""

            def __init__(self, *args, **kwargs):
                print("[WARNUNG] Fake-Picamera2 aktiv aber keine echte Kamera.")

            def start(self):
                """does nothing"""
                print("[Fake] start()")

            def stop(self):
                """does nothing"""
                print("[Fake] stop()")

            def capture(self):
                """does nothing"""
                print("[Fake] capture()")
                return b"FakeBild"

        # RICHTIGES "Modul" bauen
        fake_module = types.ModuleType("picamera2")
        fake_module.Picamera2 = FakePicamera2  # type: ignore

        # In sys.modules registrieren
        sys.modules["picamera2"] = fake_module
