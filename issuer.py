import subprocess

command = [
    "docker", 
    "run", 
    "-i", 
    "--rm", 
    "-e", 
    "GOLOG_LOG_LEVEL=info", 
    "--network=host", 
    "deco:v0.8.1-rc1"
]

with open('issuer.json', 'r') as file:
    # output = subprocess.run(command, stdin=file, text=True, capture_output=True)
    output = subprocess.check_output(command, stdin=file, text=True)
    print(output)
