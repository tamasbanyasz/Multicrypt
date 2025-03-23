from colorama import Fore, Style
import concurrent.futures
import multiprocessing
import random
import time

"""
MultiProcessExecutorUnity

This script demonstrates parallel computation using multiprocessing with ProcessPoolExecutor.
It simulates tasks where each task processes a randomly generated integer and performs a 
basic counting operation (incrementing or decrementing a result variable). 

Each task:
1. Retrieves a random integer from a shared queue.
2. If negative, decrements the result by its absolute value.
3. If positive, increments the result accordingly.
4. Returns the computed result.

The main function:
1. Generates 10 random integers in a given range.
2. Distributes these tasks among multiple processes.
3. Collects and prints the results along with execution time.

"""

class MultiProcessExecutorUnity:
    def __init__(self):
        self.result = 0  # Stores computed results

    def compute_task(self, task_id, queue):
        """
        Processes a single task by retrieving a value from the queue and performing 
        simple arithmetic operations (incrementing or decrementing self.result).
        """
        value_from_queue = queue.get()
        #print(f"\33[1mStarting task\33[0m", Fore.RED +f'{task_id}'+ Style.RESET_ALL, f"\33[1m...\33[0m")

        if value_from_queue < 0:
            for _ in range(1, abs(value_from_queue)):
                self.result -= 1
            #print(f"\33[1mFinished task\33[0m", Fore.RED +f'{task_id}'+ Style.RESET_ALL)

        elif value_from_queue > 0:
            for _ in range(1, value_from_queue + 1):
                self.result += 1
            #print(f"\33[1mFinished task \33[0m", Fore.RED +f'{task_id}'+ Style.RESET_ALL)

        return self.result

    def multiprocessing_executor_task(self, start_value, end_value):
        """
        Manages multiprocessing execution:
        1. Generates 10 random values between start_value and end_value.
        2. Assigns each value to a separate process.
        3. Collects and prints the results.
        """
        with multiprocessing.Manager() as manager:

            queue = manager.Queue()

            # Generate random values and put them in the queue
            for _ in range(10):
                queue.put(random.randint(start_value, end_value))

            start_time = time.time()  
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(self.compute_task, t_id, queue) for t_id in range(10)]
                results = []

                for process_id, future in enumerate(concurrent.futures.as_completed(futures)):
                    #print(f"\33[1mProcessing task \33[0m", Fore.RED +f'{process_id+1}'+ Style.RESET_ALL)
                    result = future.result()
                    #print(f"\33[1mGot result from task \33[0m", Fore.RED +f'{process_id+1}: {result:_}'+ Style.RESET_ALL)
                    results.append(result)

            print("\n\33[1mThe results with Executor: \33[0m", Fore.RED +f'{results}'+ Style.RESET_ALL)
            print(f"Finished in {(time.time() - start_time):.2f} seconds.")

            return results


if __name__ == "__main__":
    MultiProcessExecutorUnity()

