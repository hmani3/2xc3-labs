from auxiliary.rbt import *

class RBNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def get_brother(self):
        if self.parent.right == self:
            return self.parent.left
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
         return "(" + str(self.value) + "," + self.colour + ")"

    def rotate_right(self):
        left_child = self.left

        # self takes on left_child's right subtree
        self.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = self

        # left_child takes self's place 
        left_child.parent = self.parent
        if self.parent is not None:
            if self.is_left_child():
                self.parent.left = left_child
            else:
                self.parent.right = left_child

        # self becomes right child of left_child
        left_child.right = self
        self.parent = left_child

    def rotate_left(self):
        right_child = self.right

        # self takes on right_child's left subtree
        self.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = self

        # right_child takes self's place in the tree
        right_child.parent = self.parent
        if self.parent is not None:
            if self.is_left_child():
                self.parent.left = right_child
            else:
                self.parent.right = right_child

        # self becomes left child of right_child
        right_child.left = self
        self.parent = right_child
      



class RBTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)
    fix = fix
    