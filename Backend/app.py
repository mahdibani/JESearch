import subprocess
import sys

def run_services():
    services = [
        {"name": "Search", "file": "search_service.py", "port": 8008},
        {"name": "Compare", "file": "compare_service.py", "port": 8099},
        {"name": "Generate", "file": "generate_service.py", "port": 8066}
    ]

    processes = []
    try:
        for service in services:
            processes.append(subprocess.Popen([
                sys.executable, 
                service["file"],
                "--host", "127.0.0.1",
                "--port", str(service["port"])
            ]))
            print(f"✅ Started {service['name']} service on port {service['port']}")
        
        print("\n🚀 All services running! Press Ctrl+C to stop\n")
        while True:
            pass
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    run_services()