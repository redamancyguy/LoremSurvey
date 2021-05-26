#!/usr/bin/env python
# -*- coding: utf-8 -*-
class TClassStatic(object):
    obj_num = 0
    def __init__(self, data):
        self.data = data
        TClassStatic.obj_num += 1
    def printself(self):
        print("self.data: ", self.data)
    @staticmethod
    def smethod():
        print("the number of obj is : ", TClassStatic.obj_num)
    @classmethod
    def cmethod(cls):

        print("cmethod : ", cls.obj_num)
        print(';first')
        cls.smethod()
        print('last')
def main():
    objA = TClassStatic(10)
    objB = TClassStatic(12)
    objA.printself()
    objB.printself()
    objA.smethod()
    objB.cmethod()
    print("------------------------------")
    TClassStatic.smethod()
    TClassStatic.cmethod()
if __name__ == "__main__":
    main()