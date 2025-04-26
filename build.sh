
#!/bin/bash

# Update and install necessary packages
apt-get update
apt-get install -y git cmake clang build-essential wget

# Clone llama.cpp repository
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build llama.cpp
mkdir build
cd build
cmake ..
make

# Download the quantized model
wget -c https://huggingface.co/tensorblock/orca_mini_3b-GGUF/resolve/main/orca_mini_3b-Q5_K_S.gguf

# Create the models directory
mkdir models
mv orca_mini_3b-Q5_K_S.gguf models/
