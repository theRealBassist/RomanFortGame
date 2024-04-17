import pygame
from config import *

class Stack:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        else: 
            raise IndexError("Can not pop a stack with no items")
    
    def size(self):
        return len(self.items)