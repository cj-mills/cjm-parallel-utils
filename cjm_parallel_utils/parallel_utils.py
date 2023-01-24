# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['parallel']

# %% ../nbs/00_core.ipynb 3
# Import partial from the functools module
from functools import partial

# Import the os and time modules from the Python Standard Library
import os
import time

# Import the queue module from the concurrent package
import queue

# Import the Collection generic type from the typing module
from typing import Collection

# Import the ThreadPoolExecutor and ProcessPoolExecutor classes from the concurrent.futures module
# and alias them as tpe and ppe, respectively
from concurrent.futures import ThreadPoolExecutor as tpe
from concurrent.futures import ProcessPoolExecutor as ppe

# Import the as_completed function from the concurrent.futures module
from concurrent.futures import as_completed

# Import progress_bar
from tqdm.auto import tqdm

# %% ../nbs/00_core.ipynb 5
def parallel(func, # The function to be executed
             arr:Collection, # The input collection
             max_workers:int=None, # The maximum number of workers to use
             leave=False, # Whether to leave the progress bar after completion
             use_threads=True # Whether to use threads or processes as workers
            ):
    """
    Execute the function in parallel on the elements of the input collection.
    
    Returns:
    results (list): A list of the results of the function execution
    """
    # Use the number of CPU cores if max_workers is not specified
    max_workers = os.cpu_count() if max_workers is None else max_workers
    
    if max_workers<2: 
        # Use a simple for loop if max_workers is less than 2
        results = [func(o) for o in tqdm(arr, total=len(arr), leave=leave)]
    else:
        # Use either ThreadPoolExecutor or ProcessPoolExecutor based on use_threads
        executor = tpe(max_workers) if use_threads == True else ppe(max_workers)
        
        with executor:
            # Submit the function and input to the executor
            futures = [executor.submit(func,o) for o in arr]
            results = []
            
            # Append the result of the function execution as soon as it is done
            for f in tqdm(as_completed(futures), total=len(arr), leave=leave):
                results.append(f.result())
    
    # Return the results if any of the results is not None
    if any([o is not None for o in results]): return results
