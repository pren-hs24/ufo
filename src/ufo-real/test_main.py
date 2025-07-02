"""
from tests import test_image_recognition1  # noqa: F401 # pylint: disable=unused-import
import os


print("Running test_image_recognition1...")
print(os.getcwd())
if os.path.isfile(os.getcwd() + "yolo_model_v11/my_model.pt"):
    print("Model file found.")

test_image_recognition1.test_image_recognition_one()  # noqa: F401 # pylint: disable=unused-import
"""
