# -*- coding:utf-8 -*-
"""
    Splay tree
    Question 1
    Author: Hchyeria
"""


# 定义一个 TreeNode 类 保存树的节点信息
# 包括自身的数值 和 左右孩子节点 父节点信息
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = self.right = self.parent = None


# 定义一个 BinarySearchTree 类
# 可以进行删除 插入 和 查找操作
# 其中都需要将目标节点旋转到根节点
class SplayTree:
    def __init__(self, root=None):
        self.root = root

    # 查找函数
    def find(self, value):
        current = self.root
        # 找到相同的或者到边缘 停止循环
        if not current:
            return
        while True:
            if current.val > value:
                if not current.left:
                    break
                current = current.left
            elif current.val < value:
                if not current.right:
                    break
                current = current.right
            else:
                break
        # 将该节点伸展到根节点
        self.root = splay(self.root, current)
        # 返回是否找到
        return current.val == value

    def insert(self, value: int):
        self.root = insert(self.root, value)

    def delete(self, value: int):
        # 删除之前 先找一下是否存在 并且伸展该节点
        if not self.find(value):
            return
        self.root = delete(self.root)

    def merge(self, tree):
        self.root = merge(self.root, tree)
        return self


# 旋转函数 左旋和右旋
def rotate(root, node):
    p = node.parent
    if not p:
        return root
    # 如果节点是父节点的左孩子
    # 右旋
    if p.left == node:
        p.left = temp = node.right
        node.right = p
    else:
        # 否则 左旋
        p.right = temp = node.left
        node.left = p
    # 改变父节点的指向
    node.parent = p.parent
    p.parent = node
    temp.parent = p
    # 改变父亲的父亲的孩子指向
    if node.parent:
        if node.parent.left == p:
            node.parent.left = node
        else:
            node.parent.right = node
    return root


# 伸展函数
# 把目标节点伸展到根节点
def splay(root, node):
    # 如果不是根节点 继续伸展
    while node.parent:
        p = node.parent
        g = p.parent
        # 如果存在爷爷 需要进行两次旋转
        if g:
            # 如果 父亲和节点和同在一侧 即父亲是爷爷的左孩子 节点的父亲的左孩子
            # 或者 父亲是爷爷的右孩子 节点的父亲的右孩子 则先旋转父亲再旋转节点
            # 如果不是在同一侧
            # 节点需要进行两次旋转
            root = rotate(root, p if (p == g.left) == (node == p.left) else node)
        root = rotate(root, node)
    return root


# 插入函数
def insert(root, value):
    current = root
    node = None
    # 如果还没有根节点 将新插入的节点作为根节点
    if not current:
        root = node
        return root
    # 循环找到合适的插入位置
    while True:
        # 值小于节点值 向左移 反之 向右移
        if current.val > value:
            # 如果左孩子已经为空了 找到位置 中断循环
            if not current.left:
                # 插入到左子树
                node = TreeNode(value)
                current.left = node
                node.parent = current
                # 伸展该节点
                root = splay(root, node)
                break
            # 如果还存在左子树 再继续找位置
            current = current.left
        if current < value:
            # 如果右孩子已经为空了 找到位置 中断循环
            if not current.right:
                # 插入到右子树
                node = TreeNode(value)
                current.right = node
                node.parent = current
                # 伸展该节点
                root = splay(root, node)
                break
            # 如果还存在右子树 再继续找位置
            current = current.right
    return root


# 删除函数
def delete(root):
    # 如果存在的前提下
    # 该节点已经伸展到根节点了
    ptr = root
    # 如果同时有左孩子和右孩子
    # 将左子树的根节点作为新的根节点
    # 找到左子树最大的节点
    if ptr.left and ptr.right:
        left_node = ptr.left
        root = left_node
        while left_node.right:
            left_node = left_node.right
        # 将原来根节点的右子树 变成次节点的右子树
        left_node.right = ptr.right
        ptr.right.parent = left_node
    else:
        root = ptr.left if ptr.left else ptr.right
    root.parent = None
    return root


# 因为第二题会用到合并两个集合 所以增加了一个 merge 函数
def merge(root, tree):
    if not root and not tree:
        return
    if not tree or root:
        return root if root else tree.root
    tree = tree.root
    ptr = root
    while True:
        if tree.val < root.val:
            if not ptr.left:
                ptr.left = tree
                tree.parent = ptr
                root = splay(root, tree)
                break
            ptr = ptr.left
        else:
            if not ptr.right:
                ptr.right = tree
                tree.parent = ptr
                root = splay(root, tree)
                break
            ptr = ptr.right
    return root