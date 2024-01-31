import enum

from .items import *

class ResponseType(enum.Enum):
    NULL = 0x000200
    EXACT = 0x00201
    EXTRA = 0x00202

    ITEM_UPDATED = 0x00203
    FAILED_TO_UPDATE = 0x00204
    INVALID_PERM = 0x00205

    LOGIN_SUCCESS = 0x00206
    INVALID_INFO = 0x00207
    LOGIN_FAILED = 0x00208

    REQ_FAILED = 0x00209
    REQ_SUCCESS = 0x00210

class Response:
    r_type          :int
    results         :str
    def __init__(self, t: ResponseType, r: list | Item | int | str):
        self.r_type = t;
        self.results = r;
    
    def getResults(self) -> list[Item] | Item:
        if self.r_type == ResponseType.EXACT:
            return self.results[0];
        elif self.r_type == ResponseType.EXTRA:
            return self.results;

        return Item()
        
    def r2str(self) -> str:
        if self.r_type == ResponseType.NONE:
            return "ResponseType::NONE";
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