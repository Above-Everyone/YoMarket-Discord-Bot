import requests, enum

class YW_INFO_LOGS:		
    price           :str
    approve         :str
    approved_by     :str
    timestamp       :str
    def __init__(self, arr: list[str]):
        self.price = arr[0]
        self.approve = arr[1]
        self.approved_by = arr[2]
        self.timestamp = arr[3]


class Item:
    idx             :int
    """
        General Item Information
    """
    name   			:str
    id     			:int
    url    			:str
    price  			:str
    update 			:str

    """
        Actions you can do with the ITEM
    """
    is_tradable 	:int
    is_giftable 	:int

    """
        In-store Information
    """
    in_store       	:bool
    store_price    	:str
    gender         	:str
    xp             	:str
    category       	:str

    ywinfo_prices	:list[YW_INFO_LOGS]

    def __init__(self, arr: list[str]):
        if len(arr) > 4:
            self.name           = arr[0];
            self.id             = arr[1];
            self.url            = arr[2];
            self.price          = arr[3];
            self.update         = arr[4];
            self.is_tradable    = arr[5];
            self.is_giftable    = arr[6];
            self.in_store       = arr[7];
            self.store_price    = arr[8];
            self.gender         = arr[9];
            self.xp             = arr[10];
            self.category       = arr[11];
    def __repr__(self):
        return f"('{self.name}','{self.id}','{self.url}','{self.price}','{self.update}')"
    
    def to_str(self):
        return f"{self.name} | {self.id} | {self.price} | {self.update}"

    def parse_prices(self, content: str) -> None:
        yw_db_price = [];
        lines = content.split("\n");

        for line in lines:
            if len(line) > 3:
                yw_db_price.append(YW_INFO_LOGS(line.split(",")));

        self.ywinfo_prices = yw_db_price

class ResponseType(enum.Enum):
    NULL                = 0x000200
    EXACT               = 0x00201
    EXTRA               = 0x00202

    ITEM_UPDATED        = 0x00203
    FAILED_TO_UPDATE    = 0x00204
    INVALID_PERM        = 0x00205

    LOGIN_SUCCESS       = 0x00206
    INVALID_INFO        = 0x00207
    LOGIN_FAILED        = 0x00208

    REQ_FAILED          = 0x00209
    REQ_SUCCESS         = 0x00210

class Response:
    r_type          :int
    results         :str
    def __init__(self, t: ResponseType, r: list | Item | int | str):
        self.r_type = t;
        self.results = r;
    
    def __repr__(self):
        return "Response()"
    
    def __str__(self):
        return f"{self.r_type}\n\t=> {self.results}"
    
    def getResults(self) -> list[Item] | Item:
        if self.r_type == ResponseType.EXACT:
            return self.results[0];
        elif self.r_type == ResponseType.EXTRA:
            return self.results;

        return Item()
        
    def r2str(self) -> str:
        if self.r_type == ResponseType.NULL:
            return "ResponseType::NULL";
        if self.r_type == ResponseType.EXACT:
            return "ResponseType::EXACT";
        if self.r_type == ResponseType.EXTRA:
            return "ResponseType::EXTRA";
        if self.r_type == ResponseType.ITEM_UPDATED:
            return "ResponseType::ITEM_UPDATED";
        if self.r_type == ResponseType.FAILED_TO_UPDATE:
            return "ResponseType::FAILED_TO_UPDATE";
        if self.r_type == ResponseType.REQ_FAILED:
            return "ResponseType::REQ_FAILED";
        if self.r_type == ResponseType.REQ_SUCCESS:
            return "ResponseType::REQ_SUCCESS";

        return "";

class Items:
    """
        API Endpoints
    """
    _STATISTICS_ENDPOINT       = "https://backup.yomarket.info/statistics";
    _SEARCH_ENDPOINT           = "https://backup.yomarket.info/search?q=" ;
    # _SEARCH_ENDPOINT_ALT       = "http://167.114.155.204:8080/search?q=" ;
    _CHANGE_ENDPOINT           = "https://backup.yomarket.info/change?id=";
    _PRICE_LOGS_ENDPOINT       = "https://backup.yomarket.info/price_logs";
    _SUGGESTION_LOGS_ENDPOINT  = "https://backup.yomarket.info/all_suggestion";
    _SAVE_ENDPOINT             = "https://backup.yomarket.info/save";
    Response: Response
    query: str
    
    def __init__(self):
        pass

    def searchItem(self, query: str) -> Response:
        api_resp = requests.get(f"{self._SEARCH_ENDPOINT}{query}").text

        if api_resp == "[ X ] Error, You must enter an Item name or ID":
            return Response(ResponseType.REQ_FAILED, 0);

        searchErrors = ["[ X ] Error, You must enter an Item name or ID", f"[ X ] Error, No item was found for {query}"];

        if api_resp in searchErrors or "[ X ]" in api_resp:
            return Response(ResponseType.NULL, 0);

        if "\n" not in api_resp:
            return Response(ResponseType.EXACT, Item(api_resp.replace("'", "").replace("[", "").replace("]", "").split(",")));

        lines = api_resp.split("\n")

        if "\n" in api_resp:
            if len(lines[1].split(",")) == 4:
                content = api_resp.replace(f"{lines[0]}", "");

                item_info = lines[0].replace("[", "").replace("]", "").replace("'", "").split(",");

                item = Item(item_info);
                item.parse_prices(content)

                return Response(ResponseType.EXACT, item);
            else: pass
    
        self.found = [];
        for line in lines:
            info = line.replace("[", "").replace("]", "").replace("'", "").split(",");
            if len(info) < 5: break
            if len(info) >= 5:
                self.found.append(Item(info));

        if len(self.found) == 1:
            return Response(ResponseType.EXACT, self.found[0]);

        if len(self.found) > 1:
            return Response(ResponseType.EXTRA, self.found);

        return Response(ResponseType.NULL, 0)
    
    def changePrice(self, item_id, price, ip="5.5.5.5"):
        api_resp = requests.get(f"{self._CHANGE_ENDPOINT}{str(item_id)}", {"price": price, "ip": ip})

        if not api_resp:
            return Response(ResponseType.REQ_FAILED, 0)

        if api_resp.text == "[ X ] Error, You aren't a manager to change price. Price has been suggested to admins to investigate....":
            return Response(ResponseType.INVALID_PERM, 0)

        if api_resp.text == f"[ X ] Error, failed to change price on {item_id} {price}...!":
            return Response(ResponseType.FAILED_TO_UPDATE, 0)

        if "[ + ]" in api_resp.text and "successfully" in api_resp.text:
            return Response(ResponseType.ITEM_UPDATED, 0)

        return Response(ResponseType.NULL, 0)