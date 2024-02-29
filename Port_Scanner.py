import socket
import threading

# Create a lock to synchronize print statements
print_lock = threading.Lock()

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket setup

    try:
        sock.connect((host, port)) #Connect to host and port.
    except socket.error:
        return False
    else:
        return True
    finally:
        sock.close()

def find_port_info(port, filename):
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split() #Function opens txt and iterates through, removing leading and trailing whitespaces
            if parts and parts[0] == f'{port}': #Checks if partlist is not empty, then if element of list is equal to specified port.
                return ' '.join(parts[1:]).strip()

    return "Port information not found."

def scan_port(prompt, port, filename):
    if check_port(prompt, port):
        with print_lock: #Uses print lock to ensure print statements are not interrupted by other threads.
            print(f"Port {port} is open")
            port_info = find_port_info(port, filename)   #Function checks if port is open
            print(f"Port Information: {port_info}\n")
    else:
        with print_lock:
            print(f"Port {port} is closed")

def main():
    prompt = input("Enter Host:")
    filename = "Names.txt"
    threads = []

    for port in range(0, 444):  # Considering ports from 0 to 443
        thread = threading.Thread(target=scan_port, args=(prompt, port, filename))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
