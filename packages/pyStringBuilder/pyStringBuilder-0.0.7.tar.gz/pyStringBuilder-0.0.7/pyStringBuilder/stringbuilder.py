
class StringBuilder():
    """Python equivalent of Java and C# StringBuilders to help who is used to work with them."""

    def __init__(self, obj = None):
        self._array = []
        if(obj is not None):
            self.append(obj)

    def __hash__(self):
        return hash(self._array)

    def __len__(self):
        return len(self._array)

    def __str__(self):
        return "".join(self._array)

    def __repr__(self):
        return str(self)

    def __getitem__(self, index: int):
        if(not isinstance(index, int)):
            raise ValueError("The parameter \"index\" must be an integer.")

        return self._array[index]

    def __eq__(self, other) -> bool:
        if(type(self) == type(other)):
            return self._array == other._array

        else:
            return False

    def append(self, item) -> None:
        if(isinstance(item, bool)):
            self._array.append(str(item))

        elif(isinstance(item, int)):
            self._array.append(str(item))

        elif(isinstance(item, float)):
            self._array.append(str(item))

        elif(isinstance(item, str)):
            for char in item:
                self._array.append(char)

        elif(isinstance(item, list)):
            for element in item:
                self._array.append(str(element))

        elif(isinstance(item, dict)):
            for value in item.values():
                self._array.append(str(value))

        elif(isinstance(item, StringBuilder)):
            for value in item._array:
                self._array.append(str(value))

        else:
            self._array.append(str(item))

    def append_join(self, separator: str, item: list) -> None:
        if(not isinstance(separator, str)):
            raise ValueError("The parameter \"separator\" must be a string.")

        if(not isinstance(separator, list)):
            raise ValueError("The parameter \"item\" must be a list.")

        self._array.extend(separator.join(str(x) for x in item))

    def append_line(self, string: str = None)-> None:
        if(not isinstance(string, str)):
            raise ValueError("The parameter \"string\" must be a string.")

        if(string is None):
            self.append("\n")
        else:
            self.append(string)
            self.append("\n")

    def capitalize(self) -> str:
        return str(self).capitalize()

    def char_at(self, index: int) -> str:
        if(not isinstance(index, int)):
            raise ValueError("The parameter \"index\" must be an integer.")

        return self._array[index]

    def clear(self) -> None:
        self._array.clear()

    def copy(self):
        return StringBuilder(str(self))

    def delete(self, start: int, end: int) -> None:
        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        del self._array[start:end]

    def delete_char_at(self, index: int) -> None:
        if(not isinstance(index, int)):
            raise ValueError("The parameter \"index\" must be an integer.")

        self._array.pop(index)

    def encode(self, encoding = "utf-8", errors = "strict") -> bytes:
        if(not isinstance(encoding, str)):
            raise ValueError("The parameter \"encoding\" must be a string.")

        if(not isinstance(errors, int)):
            raise ValueError("The parameter \"errors\" must be a string.")

        return str(self).encode(encoding, errors)

    def endswith(self, substring: str, start = 0, end = -1) -> bool:
        if(not isinstance(substring, str)):
            raise ValueError("The parameter \"substring\" must be a string.")

        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        return str(self).endswith(substring, start, end)

    def find(self, substring: str, start = 0, end = -1) -> int:
        if(not isinstance(substring, str)):
            raise ValueError("The parameter \"substring\" must be a string.")

        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        return str(self).find(substring, start, end)

    def index_of(self, string: str, start = 0, stop = -1) -> int:
        if(not isinstance(string, str)):
            raise ValueError("The parameter \"string\" must be a string.")

        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(stop, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        return self._array.index(string, start, stop)

    def insert(self, index: int, item) -> None:
        if(not isinstance(index, int)):
            raise ValueError("The parameter \"index\" must be an integer.")

        self._array.insert(index, str(item))

    def lower(self) -> str:
        return str(self).lower()

    def lstrip(self, chars = None) -> str:
        if(not isinstance(chars, str)):
            raise ValueError("The parameter \"chars\" must be a string.")

        return str(self).lstrip(chars)

    def remove(self, item) -> None:
        if(isinstance(item, int)):
            self._array.remove(item)

        elif(isinstance(item, float)):
            self._array.remove(item)

        elif(isinstance(item, str)):
            for char in item:
                self._array.remove(char)

        elif(isinstance(item, list)):
            for element in item:
                self._array.remove(element)

        elif(isinstance(item, dict)):
            for value in item.values():
                self._array.remove(value)

        else:
            self._array.remove(item)

    def replace(self, old: str, new: str) -> None:
        if(not isinstance(old, str)):
            raise ValueError("The parameter \"old\" must be a string.")

        if(not isinstance(new, str)):
            raise ValueError("The parameter \"new\" must be a string.")

        for item in self._array:
            item.replace(old, new)

    def reverse(self) -> None:
        self._array.reverse()

    def rstrip(self, chars = None) -> str:
        if(not isinstance(chars, str)):
            raise ValueError("The parameter \"chars\" must be a string.")

        return str(self).rstrip(chars)

    def set_char_at(self, index: int, char: str) -> None:
        if(not isinstance(index, int)):
            raise ValueError("The parameter \"index\" must be an integer.")

        if(not isinstance(char, str)):
            raise ValueError("The parameter \"char\" must be a string.")

        self._array[index] = char

    def split(self, separator: str, maxsplit = -1) -> str:
        if(not isinstance(substring, str)):
            raise ValueError("The parameter \"substring\" must be a string.")

        if(not isinstance(maxsplit, int)):
            raise ValueError("The parameter \"maxsplit\" must be an integer.")

        return str(self).split(separator, maxsplit)

    def splitlines(self, keepends=False) -> list:
        return str(self).splitlines(keepends)

    def startswith(self, substring: str, start = 0, end = -1) -> bool:
        if(not isinstance(substring, str)):
            raise ValueError("The parameter \"substring\" must be a string.")

        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        return str(self).startswith(substring, start, end)

    def strip(self, chars = None) -> str:
        if(not isinstance(chars, str)):
            raise ValueError("The parameter \"chars\" must be a string.")

        return str(self).strip(chars)

    def sub_sequence(self, start: int, end: int = None) -> str:
        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        if(end == None):
            end = (len(self) - 1)

        return self._array[start:end]

    def substring(self, start: int, end: int = None) -> str:
        if(not isinstance(start, int)):
            raise ValueError("The parameter \"start\" must be an integer.")

        if(not isinstance(end, int)):
            raise ValueError("The parameter \"end\" must be an integer.")

        if(end == None):
            end = (len(self) - 1)

        return "".join(self._array[start:end])

    def swapcase(self) -> str:
        return str(self).swapcase()

    def upper(self) -> str:
        return str(self).upper()
