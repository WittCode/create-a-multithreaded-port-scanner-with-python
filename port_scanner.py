# Library for asynchronously executing functions.
# The ThreadPoolExecutor does the asynchronous execution with threads.
from concurrent.futures import ThreadPoolExecutor
# Library for working with sockets. We will use it to attempt to form a TCP connection.
import socket
# Library for working with time. We will use it to calculate how long the application took to run.
import time

MAX_WORKERS = 20

# 0-10000
def generate_port_chunks(port_range):
  # Get the min and max port numbers from the port range
  port_ranges = port_range.split('-')
  port_chunks = []
  # Divide the port range into chunks
  chunk_size = int((int(port_ranges[1]) - int(port_ranges[0])) / MAX_WORKERS)
  # Create a nested list of port chunks to be handled by each worker
  for i in range(MAX_WORKERS):
    start = int(port_ranges[0]) + (chunk_size * i)
    end = start + chunk_size
    port_chunks.append([start, end])
  return port_chunks

def scan(ip_address, port_chunk):
  print(f"[~] Scanning {ip_address} from {port_chunk[0]} to {port_chunk[1]}.")
  # Loop through the min and max port chunks
  for port in range(int(port_chunk[0]), int(port_chunk[1])):
    # Attempt a TCP IPv4 connection to the provided port and IP address 
    try:
      scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      scan_socket.settimeout(2)
      # print(f"[~] Scanning {ip_address} on port {port}.")
      scan_socket.connect((ip_address, port))
      print(f"[!] Port {port} is open")
    # If the port is closed an exception will be thrown, capture it here
    except:
      None
      
def main():
  ip_address = '31.220.55.159'
  port_range = '0-10000'
  
  # Divide port range into chunks
  port_chunks = generate_port_chunks(port_range)
  
  # Start the timer
  start_time = time.time()
  # Submit tasks to be executed by the thread pool using map
  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(scan, [ip_address] * len(port_chunks), port_chunks)
  # Finish the timer
  end_time = time.time()
  print(f"Scanned {port_range[1]} ports in {end_time - start_time} seconds.")

if __name__ == '__main__':
  main()