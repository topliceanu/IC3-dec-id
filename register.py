import subprocess
import docker




command = [
    "docker", 
    "run", 
    "-i", 
    "--rm", 
    "-e", 
    "GOLOG_LOG_LEVEL=info", 
    "--network=host", 
    "deco_image:v0.8.1-rc1"
]

with open('prover.json', 'r') as file:
    output = subprocess.run(command, stdin=file, text=True, capture_output=True)
    print(output.stdout)
