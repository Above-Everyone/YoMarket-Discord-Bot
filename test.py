from src.guide.items import *

item_id = "ninja"
gd = Items(item_id)
response = gd.searchItem(item_id, "5.5.5.5")

print(str(response))

if response.r_type == ResponseType.NULL:
    print("[ X ] Error, No items found...!")
elif response.r_type == ResponseType.EXACT:
    print(f"{response.results.name} | {response.results.id} | {response.results.price} | {response.results.update}")
elif response.r_type == ResponseType.EXTRA:
    for item in response.results:
        print(f"{item.to_str()}")