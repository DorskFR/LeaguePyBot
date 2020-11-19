import time
import concurrent.futures

# start = time.perf_counter()

def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f'Done Sleeping {seconds} second(s)...'

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        results = [executor.submit(do_something, sec) for sec in secs]
        
        for f in concurrent.futures.as_completed(results):
            print(f.result())

# finish = time.perf_counter()
# print(f"Finished in {round(finish-start,2)} second(s)")

if __name__ == '__main__':
    main()