from src.items import *
from src.response import *

item_id = "26295"
gd = Items(item_id)

print(f"{gd.searchItem(item_id, "5.5.5.5").results}")