import json

class connect:
    def __init__(self, name="index", *, path=""):
        """ Creates the file if it doesn't exist, or opens an existing one.

            Arguments:
                name -- type: str (default: "index"),
                path -- type: str (default: "")

            Return: class
        """
        self.name = name
        self.path = path
        self.cache = []

        if self.cache.__len__() > 20:
            self.cache.pop(0)

        try:
            r = open(f"{self.path}{self.name}.cprt", "r").read()
        except FileNotFoundError:
            w = open(f"{self.path}{self.name}.cprt", "w+").write("{}")
            r = open(f"{self.path}{self.name}.cprt", "r").read()

        self.database = json.loads(r)


    def get(self, key=False, *, printf=False):
        """ Returns the self.database dictionary.

            Arguments:
                printf -- type: bool (default: False)

            Return: dict
        """
        if not key:
            if printf: print(self.database)
            return self.database
        else:
            if type(key) is str:
                if printf: print(self.database[key])
                return self.database[key]
            else:
                keys = ""
                for i in range(key.__len__()):
                    if type(i) is str:
                        keys += f"[\"{key[i]}\"]"
                    elif type(i) is int:
                        keys += f"[{key[i]}]"
                if printf: print(eval(f"self.database{keys}"))
                return eval(f"self.database{keys}")

    def save(self):
        """ Saves the database dictionary to a file. """
        return json.dump(self.database, open(f"{self.path}{self.name}.cprt", "w+"), indent=4)

    def set(self, key=False, value=None):
        """ Sets the key value.

            Arguments:
                key -- type: str or list
                value -- type: all

            Return: None
        """
        if value is None:
            self.database = key
            self.save()
        else:
            if type(key) is str:
                self.database[key] = value
                self.cache.append({"key": key, "value": value})
            else:
                keys = ""
                for i in range(key.__len__()):
                    if type(i) is str:
                        keys += f"[\"{key[i]}\"]"
                    elif type(i) is int:
                        keys += f"[{key[i]}]"
                exec(f"self.database{keys} = value")
                self.cache.append({"key": key[-1], "value": value})
            self.save()

    def append(self, key, value):
        self.get(key).append(value)
        self.save()

    def plus(self, key, value):
        result = self.get(key) + value
        self.set(key, result)
        self.save()

    def minus(self, key, value):
        result = self.get(key) - value
        self.set(key, result)
        self.save()

    def delete(self, key):
        """ Deletes the key.

            Arguments:
                key -- type: str or list

            Return: None
        """
        if type(key) is str:
            del self.database[key]
        else:
            keys = ""
            for i in range(key.__len__()):
                if type(i) is str:
                    keys += f"[\"{key[i]}\"]"
                elif type(i) is int:
                    keys += f"[{key[i]}]"    
            exec(f"del self.database{keys}")
        self.save()

    def find_cache(self, key):
        """ Returns a list of caches with the specified key.

            Arguments:
                key -- type: str

            Return: list
        """
        result = []
        for i in self.cache:
            if i["key"] == key:
                result.append(i)
        return result

    def get_cache(self, *, printf=False):
        """ Returns a list of cache.

            Arguments:
                printf -- type: bool (default: False)

            Return: list
        """
        if printf: print(self.cache)
        return self.cache
