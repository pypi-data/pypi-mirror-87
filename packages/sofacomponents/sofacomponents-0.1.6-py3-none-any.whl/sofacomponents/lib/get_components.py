import os
import subprocess

def start(sofa_path=None):
    if sofa_path is None:
        sofa_path = os.environ["CARDIAC_SOFA_PATH"]
    subprocess.call([sofa_path, os.path.join(os.path.dirname(__file__), "scene.py"), "-g", "batch"])


if __name__=="__main__":
    start()