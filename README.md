# Fellegi Sunter Record Linkage - Winkler's EM
*Implementation of  Winkler's Expectation Maximization for Fellegi Sunter Record Linkage*


#### EM - FS Model
![EM-Algo](examples/img/fsem_.png)


#### Cross Join - Record Pairs
```html
[
 ['A1', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A2', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A3', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A4', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A5', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A6', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A7', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A8', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A9', 'B12', 1.0, 1.0, 0.0, 0.0],
 ['A10', 'B12', 1.0, 1.0, 0.0, 0.0],
]
```

### Project Structure
```
fsem
|   .gitignore
|   LICENSE
|   main.py
|   README.md
|
+---data
|       RL1.csv
|       RL2.csv
|
+---examples
|   |   RL_dataset.py
|   |
|   \---__pycache__
|           RL_dataset.cpython-37.pyc
|
+---fsem
|   |   __init__.py
|   |
|   +---algorithm
|   |   |   fsem.py
|   |   |   __init__.py
|   |   |
|   |   \---__pycache__
|   |           fsem.cpython-37.pyc
|   |           __init__.cpython-37.pyc
|   |
|   +---preprocessing
|   |   |   process.py
|   |   |   __init__.py
|   |   |
|   |   \---__pycache__
|   |           process.cpython-37.pyc
|   |           __init__.cpython-37.pyc
|   |
|   +---similarity_measures
|   |   |   jaro.py
|   |   |   levenshtein.py
|   |   |   __init__.py
|   |   |
|   |   +---utils
|   |   |   |   utils.py
|   |   |   |
|   |   |   \---__pycache__
|   |   |           utils.cpython-37.pyc
|   |   |
|   |   \---__pycache__
|   |           jaro.cpython-37.pyc
|   |           levenshtein.cpython-37.pyc
|   |           __init__.cpython-37.pyc
|   |
|   \---utils
|       |   logger.py
|       |   utils.py
|       |
|       \---__pycache__
|               logger.cpython-37.pyc
|               utils.cpython-37.pyc
|
\---logs
        em-18-8-2021.log
```
