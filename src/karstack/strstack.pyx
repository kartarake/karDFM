import os

from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strlen

cdef class UnderflowError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args[0]

    def __repr__(self) -> str:
        return f'UnderflowError: {self.message}'

    def __str__(self) -> str:
        return self.message

cdef class strstack:
    cdef public int size
    cdef public int top
    cdef public char** data

    def __cinit__(self, int size):
        self.size = size
        self.top = -1
        self.data = <char**> malloc(size * sizeof(char*))
        if self.data == NULL:
            raise MemoryError(f"Unable to allocate a stack of size {self.size} in memory")
        
    def __dealloc__(self):
        for i in range(self.top + 1):
            free(self.data[i])
        free(self.data)

    cpdef void push(self, str string):
        if self.top == self.size - 1:
            raise OverflowError(f"The stack has reached the maximum size of {self.size}")
        length = len(string)
        self.data[self.top] = <char*> malloc((length + 1) * sizeof(char))
        if self.data[self.top] == NULL:
            raise MemoryError(f"Unable to allocate memory for the string {string}")
        strcpy(self.data[self.top], string.encode("utf-8"))

    cpdef str pop(self):
        if self.top == -1:
            raise UnderflowError("The stack no value to be poped out")
        bstring = self.data[self.top]
        string = bstring.decode("utf-8")
        free(bstring)
        self.top -= 1
        return string