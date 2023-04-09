from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_data_file: Path
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    raw_train_data: Path
    raw_test_data:  Path
    train_data: Path
    test_data: Path
    target_column:  str
    preprocessor_obj_file_path: Path
    