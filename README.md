This is Yunshu's solution to the coding challenge from Ommo.
## Setup and Installation

Ensure you have Python installed on your system. The python version I am using is: Python 3.8.10.

### Creating a Virtual Environment

Navigate to the project directory and create a virtual environment:

```
python -m venv venv
```

If you are using linux, to activate the environment, run
```
source venv/bin/activate
```

# How to run the code

* Install the required environment in requirements.txt.
```
pip install -r requirements.txt
```

* To save all the middle process for better analysis, run the following script in bash:
   ```
   make run
   ```
   or
   ```
   python main.py
   ```

* To quickly get the final result, run the following script in bash:
   ```
   make fast
   ```
   or
   ```
   python main.py False
   ```

# Results
After finish running the above commands, the images should be saved in the folder "image_results". These image results can greatly help understanding the questions in the coding challenge.