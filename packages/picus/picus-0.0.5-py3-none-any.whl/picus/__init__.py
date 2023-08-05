__version__ = '0.0.5'


from pathlib import Path


data_path = Path.home().joinpath('.cache/picus/data')
data_path.mkdir(parents=True, exist_ok=True)
