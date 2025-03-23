from encrypt_decrypt_task import EncryptDecryptIntegerUnity
from multip_executor_task import MultiProcessExecutorUnity
from concurrent.futures import ThreadPoolExecutor
from threading_task import TasksToThreading
from colorama import Fore, Style
from collections import deque
from threading import Thread
from pandas import DataFrame
import multiprocessing
import time


"""
Multi-threading, Multi-processing, and Encryption Demonstration

This script demonstrates a combination of multi-threading, multi-processing, and encryption 
in Python to process and manage numerical data efficiently. The program:

- Encrypts an integer input using AES encryption (EncryptDecryptIntegerUnity).
- Uses threading to modify the number by adding and removing values concurrently.
- Stores encrypted values in a DataFrame for tracking.
- Demonstrates multi-processing with a process pool executor to perform large-scale numerical computations.
- Uses thread pool executors to run multiple computation tasks simultaneously.

## Key Features and Concepts:
1. **Encryption & Secure Memory Handling:**
   - AES encryption (CBC mode) is used to securely store integer values.
   - Secure memory wiping techniques are applied to prevent data leaks.

2. **Multi-threading for Number Modification:**
   - Two separate threads are used for incrementing and decrementing the shared integer value.
   - A threading lock ensures safe concurrent modifications.

3. **Multi-processing for Heavy Computation:**
   - A process pool executor executes numerical tasks in parallel.
   - Each process receives randomized integer values and performs computations on them.

4. **Thread Pool Executor for Additional Performance Testing:**
   - Multiple executor tasks are launched concurrently to evaluate execution performance.

## Conclusion:
### **Pros:**
- **Parallel execution significantly improves performance**, particularly for CPU-intensive tasks.
- **Threading provides quick number updates** while ensuring thread safety with locks.
- **Encryption and secure memory wiping enhance data security** when storing sensitive values.
- **Combining multi-threading and multi-processing allows handling various workloads effectively**.

### **Cons:**
- **Threading has limitations due to Python's GIL**, making it less effective for pure CPU-bound tasks.
- **Process management overhead can reduce efficiency** for smaller tasks or if improperly used.
- **Encryption adds computational cost**, which may slow down performance in high-throughput scenarios.

### **Impact of Stronger Hardware:**
- A **CPU with more cores** will improve multi-processing efficiency, reducing execution time.
- **More RAM and faster memory access** will enhance encryption and DataFrame operations.
- **High-speed storage (SSD/NVMe) may improve overall data handling and reduce I/O bottlenecks.**

Overall, this approach is well-suited for workloads that require **a balance of security, concurrency, and heavy 
computation**, but careful optimization is necessary to avoid excessive overhead.
"""

def main():
    # Initialize task handling units
    crypting_unit = EncryptDecryptIntegerUnity()
    multiprocess_executor_unit = MultiProcessExecutorUnity()
    tasks_to_threadings_unit = TasksToThreading()
    
    # Create a DataFrame to store encrypted integers
    encrypted_integers_in_df = DataFrame(columns=["Integers in bytes"])
    
    # Get user input and encrypt the integer
    user_input = int(input("\33[1mGive an integer to add DataFrame: \33[m"))
    start_time = time.time()
    encrypted_value = crypting_unit.encrypt_integer_secure(user_input)
    encryption_time = time.time() - start_time
    
    # Store the encrypted value in the DataFrame
    encrypted_integers_in_df.loc[len(encrypted_integers_in_df), "Integers in bytes"] = encrypted_value
    work_number = multiprocessing.Value('i', user_input)
    
    while True:
        print("\n\33[1mBeginning of the while loop, the number is: \33[0m", f"\33[41m {work_number.value}\33[0m")
        
        # Get user input
        user_add_value = int(input("\n\33[1mUser value to add: \33[0m"))
        user_remove_value = int(input("\33[1mUser value to remove: \33[0m"))
        
        # Perform operations using threading
        start_time = time.time()
        print("\nThreading...")
    
        task_user_add = Thread(target=tasks_to_threadings_unit.user_add, args=(work_number, user_add_value))  
        task_remove = Thread(target=tasks_to_threadings_unit.remove_from_number, args=(work_number, user_remove_value))
        
        task_user_add.start()
        task_remove.start()
        
        task_user_add.join()
        task_remove.join()
        
        threading_time = time.time() - start_time
        print("\n\33[31mAfter threading the number is: \33[0m", f"\33[41m {work_number.value} \33[0m")
        
        # Encrypt the modified value and update the DataFrame
        start_time = time.time()
        encrypted_integers_in_df.loc[len(encrypted_integers_in_df) - 1, "Integers in bytes"] = crypting_unit.encrypt_integer_secure(work_number.value)
        encryption_time = time.time() - start_time
        
        print("\n\33[1mDataFrame:\33[0m")
        print(f"\33[1m{encrypted_integers_in_df}\33[0m")
        
        # Decrypt the last encrypted value from DataFrame
        start_time = time.time()
        decrypted_value = crypting_unit.decrypt_integer_secure(encrypted_integers_in_df.iloc[-1]["Integers in bytes"])
        decryption_time = time.time() - start_time
        
        print(f"\n\33[31mModified decrypted value from DataFrame is: \33[0m \33[41m {decrypted_value} \33[0m")
        print("Threading time:", threading_time)
        print("Encryption time:", encryption_time)
        print("Decryption time:", decryption_time)
        
        # Execute multiprocessing task
        print("\n Single task with Executor ...")
        start_time = time.time()
        result_of_multip_executor = multiprocess_executor_unit.multiprocessing_executor_task(-20_000_000, 20_000_000)
        execution_time = time.time() - start_time
        
        print("\n\33[31mThe summarized result: \33[0m", format(sum(result_of_multip_executor), '_d'))
        print("Execution time:", execution_time)
        print("... end single Executor.")
        
        # Execute tasks in parallel using ThreadPoolExecutor
        print("\n Executors in Threading (2 Thread) ...")
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(multiprocess_executor_unit.multiprocessing_executor_task, -20_000_000, 20_000_000)
            executor.submit(multiprocess_executor_unit.multiprocessing_executor_task, -20_000_000, 20_000_000)
        threading_executor_time = time.time() - start_time
        
        print("Execution time:", threading_executor_time)
        print("\n ... end Executors with Threading (2 Thread).")
        

if __name__ == "__main__":
    main()
    