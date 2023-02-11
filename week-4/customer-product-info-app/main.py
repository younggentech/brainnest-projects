###########################################################
# This script will convert text orders in orders.txt file #
# to json like orders list to orders.json file            #
###########################################################

import re
import json

orders_dict = []
with open("orders.txt", "r") as orders_file:
    while order := orders_file.readline():
        _items = re.search(":(.+?)and", order).group(0).lstrip(": ").rstrip(" and")
        orders_dict.append(
            {
                "order_number": re.search("[0-9]+", order).group(0),
                "customer_name": re.search("customer [a-zA-Z]*", order).group(0).split()[1],
                "items": {item.split()[0]: item.split()[2] for item in _items.split(",")},
                "address": re.search("address: (.+?)*", order).group(0).lstrip("address: ").strip()
            }
        )

with open("orders.json", "w") as orders_json:
    orders_json.write(json.dumps(orders_dict, indent=4))
