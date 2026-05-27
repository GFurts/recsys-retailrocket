"""Environment validation script.

Run this script to verify that all required environment variables
are correctly set and the project dependencies are available.
"""

import sys


def validate_settings() -> bool:
    """Validate that all settings load correctly from .env."""
    try:
        from recsys.config.settings import settings

        print("✓ Settings loaded successfully")
        print(f"  MLflow URI:        {settings.mlflow_tracking_uri}")
        print(f"  Experiment name:   {settings.mlflow_experiment_name}")
        print(f"  Data raw path:     {settings.data_raw_path}")
        print(f"  Data processed:    {settings.data_processed_path}")
        print(f"  Random seed:       {settings.random_seed}")
        print(f"  Batch size:        {settings.batch_size}")
        print(f"  Learning rate:     {settings.learning_rate}")
        print(f"  Num epochs:        {settings.num_epochs}")
        return True
    except Exception as e:
        print(f"✗ Settings error: {e}")
        return False


def validate_imports() -> bool:
    """Validate that all required libraries are importable."""
    libraries = {
        "torch": "PyTorch",
        "sklearn": "Scikit-learn",
        "mlflow": "MLflow",
        "pandas": "Pandas",
        "numpy": "NumPy",
    }

    all_ok = True
    for module, name in libraries.items():
        try:
            __import__(module)
            print(f"✓ {name} available")
        except ImportError:
            print(f"✗ {name} NOT found")
            all_ok = False
    return all_ok


def validate_gpu() -> None:
    """Check GPU availability."""
    import torch

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"✓ GPU available: {gpu_name}")
    else:
        print("⚠ GPU not available, using CPU")


def main() -> None:
    """Run all validations and exit with appropriate code."""
    print("=" * 50)
    print("Environment Validation")
    print("=" * 50)

    print("\n[1] Checking dependencies...")
    imports_ok = validate_imports()

    print("\n[2] Checking settings...")
    settings_ok = validate_settings()

    print("\n[3] Checking GPU...")
    validate_gpu()

    print("\n" + "=" * 50)
    if imports_ok and settings_ok:
        print("✓ Environment is ready!")
        sys.exit(0)
    else:
        print("✗ Environment has issues. Fix errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
