import time

# Allocate approximately 2 GB of memory
memory = []

try:
    while True:
        memory.append(bytearray(100 * 1024 * 1024))  # 100 MB
        print(f"Allocated: {len(memory) * 100} MB")
        time.sleep(1)

except KeyboardInterrupt:
    print("Memory test stopped.")