import time

# Print initial lines
print("Line 1: Loading...")
print("Line 2: Processing...")
print("Line 3: Status...")

for i in range(11):
    time.sleep(0.5)
    
    # Move up 3 lines and rewrite
    print("\033[3A", end='')  # Move up 3 lines
    print(f"\033[KLine 1: Progress {i*10}%")
    print(f"\033[KLine 2: Items processed: {i}")
    print(f"\033[KLine 3: Status: {'█' * i}", flush=True)
