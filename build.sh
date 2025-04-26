# Clone llama.cpp
echo "Cloning llama.cpp..."
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Print the current directory after cloning
echo "Current directory after cloning llama.cpp:"
pwd
ls -R

# Build llama.cpp
echo "Building llama.cpp..."
mkdir build
cd build
cmake ..
make

# Print the directory structure after build
echo "Directory structure after build:"
pwd
ls -R

# Download the quantized model
echo "Downloading the quantized model..."
cd ~
wget -c https://huggingface.co/tensorblock/orca_mini_3b-GGUF/resolve/main/orca_mini_3b-Q5_K_S.gguf

# Print the current directory where the model is downloaded
echo "Current directory after downloading the model:"
pwd
ls -l

# Move the model to the models folder
echo "Moving the model to the models folder..."
cd ~/llama.cpp
mkdir models
mv ~/orca_mini_3b-Q5_K_S.gguf models/

# Verify that the model is in place
echo "Directory structure after moving the model:"
pwd
ls -R