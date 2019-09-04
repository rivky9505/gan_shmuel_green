
from tavern.core import run

success = run("test_api.tavern.yaml")
print(str(success))
if not success:
    print("Error running tests")

if success:
	print("GOOOD JOOB")
