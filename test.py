from src.items import *
from src.response import *

item_id = "26295"
gd = Items(item_id)
response = gd.searchItem(item_id, "5.5.5.5")

if response.r_type == ResponseType.NONE:
    print("[ X ] Error, No items found...!")
elif response.r_type == ResponseType.EXACT:
    print(f"{response.results.name} | {response.results.id} | {response.results.price} | {response.results.update}")
elif response.r_type == ResponseType.EXTRA:
    for item in response.results:
        print(f"{item.to_str()}")