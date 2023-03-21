echo [$(date)]: "START"
echo [$(date)]: "Creating conda enviroment"

conda create --prefix ./env python==3.10 -y
echo [$(date)]: "Activating environment"

#source ~/miniconda3/etc/profile.d/conda.sh
conda activate ./env
echo [$(date)]: "Installing dev requirements"

pip install -r requirements.txt