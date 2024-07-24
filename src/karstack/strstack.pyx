from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strlen

cdef class UnderflowError(Exception):
    """The Underflow Error class for the following stack.
    """    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args[0]

    def __repr__(self) -> str:
        return f'UnderflowError: {self.message}'

    def __str__(self) -> str:
        return self.message

cdef class strstack:
    """The string stack for stack module.
    """    
    cdef int maxsize
    cdef int top
    cdef char** data

    def __cinit__(self, int maxsize):
        """The class for handling string stack in c arrays in primary memory.

        Args:
            maxsize (int): The maximum size / length of the stack.

        Raises:
            MemoryError: Raised when there is not enough memory for the operation.
        """        
        self.maxsize = maxsize
        self.top = -1
        self.data = <char**> malloc(maxsize * sizeof(char*))
        if self.data == NULL:
            raise MemoryError(f"Unable to allocate a stack of size {self.maxsize} in memory")
        
    def __dealloc__(self):
        """To free up memory after usage.
        """        
        for i in range(self.top + 1):
            free(self.data[i])
        free(self.data)

    cpdef void push(self, str string):
        """The function to push a string to the top of stack implemented by c array.

        Args:
            string (str): The string that you want to push into stack.

        Raises:
            OverflowError: Raised when trying to push an item to stack of maximum size.
            MemoryError: Raised when there is error alloting memory for a string.
        """        
        if self.top == self.size - 1:
            raise OverflowError(f"The stack has reached the maximum size of {self.maxsize}")
        length = strlen(string)
        self.data[self.top] = <char*> malloc((length + 1) * sizeof(char))
        if self.data[self.top] == NULL:
            raise MemoryError(f"Unable to allocate memory for the string {string}")
        strcpy(self.data[self.top], string.encode("utf-8"))

    cpdef str pop(self):
        """To pop the string on the top of the stack and return it to the call statement. This deletes the item in the stack.

        Raises:
            UnderflowError: Raised when trying to pop an item when the stack is empty.

        Returns:
            str: The string on the top of the stack.
        """        
        if self.top == -1:
            raise UnderflowError("The stack has no value to be poped out")
        bstring = self.data[self.top]
        string = bstring.decode("utf-8")
        free(bstring)
        self.top -= 1
        return string

    cpdef str peek(self):
        """To peek and return the string on the top of stack. This does not remove the string from the stack.

        Raises:
            UnderflowError: Raised when trying to peek an empty stack.

        Returns:
            str: The string on the top of the stack.
        """        
        if self.top == -1:
            raise UnderflowError("The stack has no value to be poped out")
        string = self.data[self.top].decode("utf-8")
        return string

    cpdef int size(self):
        """Returns the size of stack currently. That is, the number of items in the stack.

        Returns:
            int: Size of stack rn.
        """        
        return self.top + 1

    cpdef int percentage(self):
        """Returns the percentage of how much the stack has been filled.

        Returns:
            float: The percentage stack has been filled.
        """        
        return self.size() / self.maxsize * 100

    cpdef bint is_empty(self):
        """Returns True if the stack is empty and returns False if not.

        Returns:
            bool: True / False depending on the case.
        """        
        return self.top == -1
    
    cpdef bint is_full(self):
        """Returns True if the stack is full, and returns False if not.

        Returns:
            bool: True / False depending on the case.
        """        
        return self.top == self.maxsize - 1

    def __repr__(self) -> str:
        return f"String stack: {self.top + 1}/{self.maxsize}"