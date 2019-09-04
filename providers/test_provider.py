
from tavern.core import run
from termcolor import colored


get_health_status = run("./autotesting/test_get_health.tavern.yaml")
get_rates_status = run("./autotesting/test_get_rates.tavern.yaml")
get_truck_status = run("./autotesting/test_get_truck.tavern.yaml")
post_provider_status = run("./autotesting/test_post_provider.tavern.yaml")
post_rates_status = run("./autotesting/test_post_rates.tavern.yaml")
post_truck_status = run("./autotesting/test_post_truck.tavern.yaml")
put_provider_status = run("./autotesting/test_put_provider.tavern.yaml")
put_truck_status = run("./autotesting/test_put_truck.tavern.yaml")

if get_health_status == 0:
    print("[GET][HEALTH]:" + colored("SUCCED", 'green'))
else:
    print("[GET][HEALTH]:" + colored("FAILED", 'red'))

if get_rates_status == 0:
    print("[GET][RATES]:" + colored("SUCCED", 'green'))
else:
    print("[GET][RATES]:" + colored("FAILED", 'red'))

if get_truck_status == 0:
    print("[GET][TRUCK]:" + colored("SUCCED", 'green'))
else:
    print("[GET][TRUCK]:" + colored("FAILED", 'red'))

if post_provider_status == 0:
    print("[POST][PROVIDER]:" + colored("SUCCED", 'green'))
else:
    print("[POST][PROVIDER:" + colored("FAILED", 'red'))

if post_rates_status == 0:
    print("[POST][RATES]:" + colored("SUCCED", 'green'))
else:
    print("[POST][RATES]:" + colored("FAILED", 'red'))

if post_truck_status == 0:
    print("[POST][TRUCK]:" + colored("SUCCED", 'green'))
else:
    print("[POST][TRUCK]:" + colored("FAILED", 'red'))

if put_provider_status == 0:
    print("[PUT][PROVIDER]:"  + colored("SUCCED", 'green')) 
else:
    print("[PUT][PROVIDER]:" + colored("FAILED", 'red'))

if put_truck_status == 0:
    print("[PUT][TRUCK]:" + colored("SUCCED", 'green'))
else:
    print("[PUT][TRUCK]:" + colored("FAILED", 'red'))

# success = run("test_api.tavern.yaml")
# print(str(success))
# if not success:
#     print("Error running tests")

# if success:
# 	print("GOOOD JOOB")
# #http://0.0.0.0:5000/truck?id=222-33-111&name=Provider 1
# ---