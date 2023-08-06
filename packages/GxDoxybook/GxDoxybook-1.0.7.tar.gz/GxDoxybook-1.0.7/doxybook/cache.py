
class Cache:
    def __init__(self):
        self.cache = {}
        self.cache_on_name = {}

    def add(self, key: str, value):
        self.cache[key] = value

    def get(self, key: str):
        if key in self.cache:
            return self.cache[key]
        else:
            raise IndexError('Key: ' + key + ' not found in cache!')

    def add_onname(self, key: str, value):
        self.cache_on_name[key] = value #add by jiangzq

    def get_on_name(self, key: str):
        if key in self.cache_on_name:
            return self.cache_on_name[key]
        else:
            #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            print(key)
            #for key,value in self.cache_on_name.items():
            #    print(key,":",value.name)
            #raise IndexError('Key: ' + key + ' not found in cache!')
            print('Worning: Key: ' + key + ' not found in cache!')
            return None
