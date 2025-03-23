from colorama import Fore, Style
from threading import Lock

"""
TasksToThreading

This script demonstrates thread-safe operations using the `threading` module in Python.
It provides methods for safely modifying a shared numeric variable using multiple threads.

Key Features:
1. **Thread-Safe Incrementing (`user_add`)**:
   - Increments a shared `number.value` variable safely inside a loop.
   - Uses a lock to prevent race conditions.

2. **Thread-Safe Decrementing (`remove_from_number`)**:
   - Decrements the shared `number.value` variable.
   - Uses a lock to ensure only one thread modifies the variable at a time.

Both operations use `threading.Lock()` to ensure safe concurrent access to `number.value`.

"""

class TasksToThreading:
    def __init__(self):
        self.lock = Lock()  # Lock to ensure thread safety

    def user_add(self, number, user_value):
        """
        Safely increments the `number.value` by `user_value` times.
        Uses a lock to prevent race conditions.
        """
        with self.lock:
            for _ in range(user_value):
                number.value += 1
                #print("\n\33[1mAfter user added, the work_number is: \33[0m", Fore.RED + f'{number.value}' + Style.RESET_ALL)

    def remove_from_number(self, number, user_value):
        """
        Safely decrements the `number.value` by `user_value` times.
        Uses a lock to ensure thread safety.
        """
        with self.lock:
            for _ in range(user_value):
                number.value -= 1
                #print("\n\33[1mRemove from work_number: \33[0m", Fore.RED + f'{number.value}' + Style.RESET_ALL)


if __name__ == "__main__":
    TasksToThreading()

    