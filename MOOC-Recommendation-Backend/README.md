### Prerequisites

1. Install anaconda package distribution system
2. Create a virtual python 3.8 environment using anaconda.  
    `conda create -n {env_name} python=3.8`
3. Activate the environment just created  
    `conda activate {env_name}`
4. Run following commands to install required packages.  
    `pip install -r requirements.txt`  
    `conda install openjdk=8.0.312 -c conda-forge`  
    `conda install -c conda-forge findspark`

### Run backend

1. Run following command to start backend  
    `python main.py`