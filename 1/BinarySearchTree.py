# -*- coding:utf-8 -*-
"""
    Binary search tree
    Question 1
    Author: Hchyeria
"""


# 定义一个 TreeNode 类 保存树的节点信息
# 包括自身的数值 和 左右孩子节点信息
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return repr(self.val)


# 定义一个 BinarySearchTree 类
# 可以进行删除和插入操作
class BinarySearchTree:
    def __init__(self, root=None):
        self.root = root

    def insert(self, value: int):
        self.root = insert(value, self.root)

    def delete(self, value: int):
        self.root = delete(value, self.root)


# 插入函数
def insert(value: int, root):
    new_node = TreeNode(value)
    # 如果还没有根节点 让新插入的节点成为根节点
    if root is None:
        root = new_node
    else:
        # 如果已经有根节点
        # 让新插入的值与节点的值进行比较
        # 如果新插入的节点值小 指针向左孩子移动
        # 如果新插入的节点值大 指针向右孩子移动
        ptr = root
        # 缓存找到的新插入的节点的父节点用
        parent = None
        while ptr and new_node.val != ptr.val:
            parent = ptr
            ptr = ptr.left if new_node.val < ptr.val else ptr.right
        # 如果找到和新插入节点值相同的节点 则不继续执行直接返回
        if not ptr:
            # 没有相同的值
            # 如果新插入的节点的值小于父节点 则将其作为父节点的左孩子
            # 反之 则作为右孩子
            if new_node.val < parent.val:
                parent.left = new_node
            else:
                parent.right = new_node
    return root


# 删除函数
def delete(value: int, root):
    # 如果还没有根节点 直接返回
    if not root:
        return
    # 递归找到和指定的要删除的值相同的节点
    # 如果值比节点的值大 则指针向右移
    # 反之 则向左移
    if root.val < value:
        root.right = delete(value, root.right)
    elif root.val > value:
        root.left = delete(value, root.left)
    else:
        # 找到节点后 有三种情况
        # 1. 节点同时有左孩子和右孩子
        # 2. 节点只有一个孩子
        # 3. 节点没有孩子
        if root.left and root.right:
            # 如果是第1种情况 找到节点右孩子的最小的值 将这个值赋给节点 再将其删除
            current = root.right
            # 找到最小的节点
            while current.left:
                current = current.left
            root.right = delete(current.val, root.right)
            root.val = current.val
        else:
            # 如果是后2种情况
            # 只有一个子树 则让其的根节点成为节点
            # 没有孩子 直接赋为 None
            root = root.left if root.left else root.right
    return root