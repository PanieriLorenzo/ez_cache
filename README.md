# ez_cache

Uncomplicated persistent cache and memoization, designed for humans.

ez_cache is not the most efficient or most fully featured caching/memoization
package out there. It's purpose is to be "good enough" for most applications, while
remaining uncomplicated. It is also human-readable, as it stores data in JSON files.

It offers multiple types of caching and memoization:
- mem_cache: a volatile cache, that is wiped after the program ends
- disk_cache: a cache that is stored on disk, and persists after program termination
- memoize: can be volatile or not depending on the backend

It has decent performance, and is thread safe.

## Roadmap

- [ ] mem_cache
- [ ] disk_cache
- [ ] memoize
- [ ] thread safety
- [ ] multiple persistance backends, including my own serialization format
