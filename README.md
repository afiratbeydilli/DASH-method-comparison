# Comparison of Rate Selection Methods of DASH (Dynamic Adaptive Streaming over HTTP)

This project simulates and compares rate selection methods in **Dynamic Adaptive Streaming over HTTP (DASH)**.

## Installation

### Prerequisites

- Python 3.8+
- PyCharm, VSCode, or any text editor

### Step 1: Clone the repository

First, clone the repository to your local machine and enter to the directory:

```sh
git clone https://github.com/afiratbeydilli/DASH-method-comparison.git
```
```sh
cd DASH-method-comparison
```

### Step 2: Create a Virtual Environment (Optional)
It's a good practice to use a virtual environment to manage dependencies & prevent cyclic dependencies.
Even though it is not mandatory, it is strongly recommended to set up a virtual environment before
installing the necessary modules.

#### Using venv (Python 3.3+)

1) Create a virtual environment:

```sh
python3 -m venv venv
```
This creates a directory named venv which contains your virtual environment.

2) Activate the virtual environment:

On Windows:

```sh
venv\Scripts\activate
```

On macOS and Linux:

```sh
source venv/bin/activate
```

### Step 3: Install Dependencies
With the virtual environment activated (or not if you skipped step 2), install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

This will install all the packages listed in the requirements.txt file.

## Usage

Enter the directory & run the main script:

```sh
cd DASH-method-comparison
```
```sh
python main.py
```

## Contributing & License

The project is prepared by Ahmet Fırat Beydilli for `EE542 - Computer Networks` course.

+ Yuan, H., Hu, X., Hou, J., Wei, X., & Kwong, S. (2019). An Ensemble Rate Adaptation Framework for Dynamic Adaptive Streaming Over HTTP. Retrieved from https://arxiv.org/abs/1912.11822
	
+ Narayan, A., et al. (2016). BOLA: Near-optimal bitrate adaptation for online videos. ACM Transactions on Networking (TON).