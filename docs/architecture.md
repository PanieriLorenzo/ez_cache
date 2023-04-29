```mermaid
graph BT

JSONBackend --> FileBackend
DiskCache -.- FileBackend
DiskCache --> Cache --> DictLike
MemCache --> Cache
memoize -.- Cache
```