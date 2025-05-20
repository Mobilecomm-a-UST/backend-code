from concurrent.futures import ThreadPoolExecutor, as_completed
from gpl_audit_tool.config.settings import Config

class ThreadPool:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=Config().get("max_threads"))
        self.futures = []  

    def submit_task(self, func, *args):
        """Submit a task to the thread pool and store the future."""
        future = self.executor.submit(func, *args)
        self.futures.append(future)

    def wait_for_completion(self):
        """Wait for all submitted tasks to complete."""
        for future in as_completed(self.futures):
            try:
                future.result()  
            except Exception as e:
                print(f"Task encountered an error: {e}")  
        self.futures.clear() 

    def shutdown(self):
        """Shuts down the thread pool."""
        self.executor.shutdown(wait=True)
