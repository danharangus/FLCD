class HashTable:
    def __init__(self, initial_size=10, load_factor=0.7):
        self.size = initial_size
        self.load_factor = load_factor
        self.table = [None] * self.size
        self.num_elements = 0

    def resize(self, new_size):
        new_table = [None] * new_size
        for element in self.table:
            if element is not None:
                key, value = element
                index = self.hash_function(key, new_size)
                while new_table[index] is not None:
                    index = (index + 1) % new_size
                new_table[index] = (key, value)
        self.size = new_size
        self.table = new_table

    def hash_function(self, key, size):
        if isinstance(key, str):
            # If the key is a string, calculate the sum of Unicode values and hash
            hash_value = sum(ord(char) for char in key)
        elif isinstance(key, int):
            # If the key is an integer, just use the key directly
            hash_value = key
            
        index = hash_value % size
        return index

    def put(self, key, value):
        if self.num_elements / self.size >= self.load_factor:
            # Resize the table when the load factor is exceeded
            self.resize(self.size * 2)

        index = self.hash_function(key, self.size)
        while self.table[index] is not None:
            index = (index + 1) % self.size
        self.table[index] = (key, value)
        self.num_elements += 1

    def get(self, key):
        index = self.hash_function(key, self.size)
        original_index = index

        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == original_index:
                break
        
        return None

    def __str__(self):
        return str(self.table)
