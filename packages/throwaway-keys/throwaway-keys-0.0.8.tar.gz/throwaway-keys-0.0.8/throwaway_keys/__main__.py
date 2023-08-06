# Modules
import platform
from datetime import datetime

from libs.colors import colored
from ext.defaults import generators

from ext.commands import run_commands
from libs.generators import generate_hash

from libs.arguments import get_length, get_rounds, uses

# CLI Commands
run_commands()

# Initialization
rounds = get_rounds()
length = get_length()

generator = uses()
generator = generators[generator] if generator else generators["sha512"]

# Hashing
start = datetime.now()
result = generate_hash(generator, rounds, length)
end = round((datetime.now() - start).total_seconds(), 2)

# End result
print("The", colored("Throwaway Keys", "yellow"), "Project")
print(f"Running Python {platform.python_version()} on {platform.system()}")
print("=" * 35)
print()

print("Hash results:")
print(" ", f"Algorithm: {generator.__name__}")
print(" ", f"Rounds: {rounds}")
print(" ", f"Requested length: {length}")
print(" ", f"Result length: {len(result)}")
print(" ", f"Completion Time: {end} second(s)")

print()
print("End result:")
print(colored(result, "green"))
