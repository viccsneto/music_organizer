#!/bin/bash
# setup_environment.sh: Setup conda environment for music-organizer
set -e

ENV_NAME="music-organizer-env"
PYTHON_VERSION=3.8

# Check for conda
if ! command -v conda &> /dev/null; then
    echo "conda could not be found. Please install Miniforge or Miniconda first."
    exit 1
fi

# Create environment if it doesn't exist
if ! conda info --envs | grep -q "$ENV_NAME"; then
    conda create -y -n "$ENV_NAME" python=$PYTHON_VERSION
fi

# Activate environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

# Install pip and project dependencies
conda install -y pip
pip install .

echo "Environment '$ENV_NAME' is ready. Activate it with: conda activate $ENV_NAME"
