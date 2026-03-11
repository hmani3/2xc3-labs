def fix(self, node):
        if node.parent is None:
            node.make_black()
            return

        while node is not None and node.parent is not None and node.parent.is_red():
            parent = node.parent
            grandparent = parent.parent

            if parent.is_left_child():
                uncle = grandparent.right

                if uncle is not None and uncle.is_red():
                    # uncle is red, recolour and move violation up
                    parent.make_black()
                    uncle.make_black()
                    grandparent.make_red()
                    node = grandparent

                else:
                    if node.is_right_child():
                        # tiangle (inner child), rotate to straighten into a line
                        node = parent
                        node.rotate_left()
                        parent = node.parent

                    # line (outer child), rotate grandparent and recolour
                    parent.make_black()
                    grandparent.make_red()
                    if grandparent.parent is None:
                        self.root = parent
                    grandparent.rotate_right()

            else:
                # Mirror image: parent is a right child
                uncle = grandparent.left

                if uncle is not None and uncle.is_red():
                    # Case 1 (mirror): Uncle is red — recolour and move violation up
                    parent.make_black()
                    uncle.make_black()
                    grandparent.make_red()
                    node = grandparent

                else:
                    if node.is_left_child():
                        # Case 2 (mirror): Triangle — rotate to straighten into a line
                        node = parent
                        node.rotate_right()
                        parent = node.parent

                    # Case 3 (mirror): Line — rotate grandparent and recolour
                    parent.make_black()
                    grandparent.make_red()
                    if grandparent.parent is None:
                        self.root = parent
                    grandparent.rotate_left()

        self.root.make_black()
                        