# -*- coding:utf-8 -*-
"""
    AVL tree
    Question 1
    Author: Hchyeria

"""


# 定义一个 TreeNode 类 保存树的节点信息
# 包括自身的数值 和 左右孩子节点信息
# 额外一个 height 信息 因为需要判断树是否平衡
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None
        self.height = 0


# 定义一个 AVLTree 类
# 可以进行删除和插入操作
class AVLTree:
    def __init__(self, root=None):
        self.root = root

    def insert(self, value):
        self.root = insert(value, self.root)

    def delete(self, value: int):
        self.root = delete(value, self.root)


# 获取高度的函数 空子树为 -1 之后往上逐渐加1
def get_height(node):
    return -1 if not node else node.height


# 返回 左子树与右子树 高度之差
def check_height(node):
    if node.left and node.right:
        return get_height(node.left) - get_height(node.right)
    elif node.left:
        return get_height(node.left) + 1
    elif node.right:
        return -(get_height(node.right) + 1)
    return 0


# 更新高度信息
def upload_height(node):
    node.height = max(get_height(node.left), get_height(node.right)) + 1


# 右旋
# 左子树与节点交换 左子树的右子树变成节点的左子树
# 更新左子树与节点的高度
def rotate_with_left(node):
    left_child = node.left
    node.left = left_child.right
    left_child.right = node
    upload_height(node)
    upload_height(left_child)
    return left_child


# 左旋
# 右子树与节点交换 右子树的左子树变成节点的右子树
# 更新右子树与节点的高度
def rotate_with_right(node):
    right_child = node.right
    node.right = right_child.left
    right_child.left = node
    upload_height(node)
    upload_height(right_child)
    return right_child


# 先左旋再右旋
# 出现在节点的右子树的左子树高出一截
def double_rotate_left(node):
    node.left = rotate_with_right(node.left)
    return rotate_with_left(node)


# 先右旋再左旋
# 出现在节点的左子树的右子树高出一截
def double_rotate_right(node):
    node.right = rotate_with_left(node.right)
    return rotate_with_right(node)


# 检查是否不平衡 需要旋转
def rotate(node):
    # 空节点直接返回
    if not node:
        return
    # 获取节点左子树与右子树高度之差
    point = check_height(node)
    # 如果平滑 只需要更新高度信息
    if abs(point) < 2:
        upload_height(node)
    # 左子树比右子树高
    elif point == 2:
        # 再检查左子树的 左子树与右子树的高度查
        # 如果左子树的 右子树高 应该进行双旋转
        if check_height(node.left) == -1:
            node = double_rotate_left(node)
        else:
            # 否则 只需要一次右旋
            node = rotate_with_left(node)
    # 右子树比左子树高
    elif point == -2:
        # 再检查右子树的 左子树与右子树的高度查
        # 如果右子树的左子树高 应该进行双旋转
        if check_height(node.right) == 1:
            node = double_rotate_right(node)
        else:
            # 否则 只需要一次左旋
            node = rotate_with_right(node)
    return node


# 插入函数
def insert(value, node):
    # 如果不存在次节点 直接将新节点作为次节点
    if not node:
        return TreeNode(value)
    # 递归插入
    # 值比节点大 递归右子树
    # 反之 递归左子树
    if node.val < value:
        node.right = insert(value, node.right)
    if node.val > value:
        node.left = insert(value, node.left)
    # 检查是否平衡
    return rotate(node)


# 删除操作时 如果同时有左子树和右子树
# 可以找到左子树最大的节点 和 右子树最小的节点 与要删除的节点进行替换
# 到底应该找哪个 需要在不破坏的平衡的条件下 判断最高的那边
# 寻找合适的删除节点
def find_replace_node(node):
    # 左边高 找左子树最大的节点
    if check_height(node) > 0:
        current = node.left
        while current.right:
            current = current.right
    # 否则 右子树最小的节点
    else:
        current = node.right
        while current.left:
            current = current.left
    return current


# 删除函数
def delete(value, node):
    # 递归找到 与值相同的节点
    if not node:
        return
    if node.val < value:
        node.right = delete(value, node.right)
    elif node.val > value:
        node.left = delete(value, node.left)
    else:
        # 如果同时有左右子树
        # 找到不破坏平衡的节点 删除
        if node.left and node.right:
            target = find_replace_node(node)
            node = delete(target.val, node)
            node.val = target.val
        else:
            node = node.left if node.left else node.right
        # 检查是否平衡
    return rotate(node)




