# coding=utf-8
"""
Author:胡立新    Version:1.0    Date:2017-5-5

Description:此模块用于解决八数码问题。
            IDA*的基本思路是：首先将初始状态结点的H值设为阈值maxH，然后进行深度优先搜索，搜索过程中忽略
            所有H值大于maxH的结点；如果没有找到解，则加大阈值maxH，再重复上述搜索，直到找到一个解。在保
            证H值的计算满足A*算法的要求下，可以证明找到的这个解一定是最优解。在程序实现上，IDA* 要比 A*
            方便，因为不需要保存结点，不需要判重复，也不需要根据 H值对结点排序，占用空间小。

Function list:
    类：CIDANode：根据启发函数有选择扩展的广度优先搜索求出八数码的最短路径的基本操作

History:
"""

import copy
import numpy as np

manhattan = (
    (0, 1, 2, 1, 2, 3, 2, 3, 4),
    (1, 0, 1, 2, 1, 2, 3, 2, 3),
    (2, 1, 0, 3, 2, 1, 4, 3, 2),
    (1, 2, 3, 0, 1, 2, 1, 2, 3),
    (2, 1, 2, 1, 0, 1, 2, 1, 2),
    (3, 2, 1, 2, 1, 0, 3, 2, 1),
    (2, 3, 4, 1, 2, 3, 0, 1, 2),
    (3, 2, 3, 2, 1, 2, 1, 0, 1),
    (4, 3, 2, 3, 2, 1, 2, 1, 0))


def calc_inversions(seq):
    """
    计算逆序数

    Args:
        seq(list):
            一维序列

    Return:
        (int)逆序数之和
    """
    num = 0
    length = len(seq)
    for i in range(length - 1):
        for j in range(i + 1, length):
            if seq[i] > seq[j]:
                num += 1
    return num


def is_solve(start_node, end_node):
    """
        判断八数码是否有解

        Arg:
            start_node(list):
                八数码的数字，空位None
            end_node(list):
                八数码的数字，空位None

        Returns:
            (bool)有解返回True,否则返回False
        """
    new_start = copy.deepcopy(start_node)
    new_end = copy.deepcopy(end_node)
    new_start.remove(None)
    new_end.remove(None)
    num1 = calc_inversions(new_start)
    num2 = calc_inversions(new_end)
    if (num1 - num2) % 2 == 0:
        return True
    else:
        return False


def calc_manh(node1, node2):
    """
    计算两个结点间的manhattan距离

    Args:
        node1(list):
            节点1，空位为None
        node2(list):
            节点2，空位为None

    Returns:
        (int)两个结点间的manhattan距离
    """
    global manhattan
    distance = 0
    for i in range(1, 9):
        idx1 = node1.index(i)
        idx2 = node2.index(i)
        distance += manhattan[idx1][idx2]
    return distance


class CIDANode(object):
    def __init__(self, node, fn_heuristic):
        """
        对象初始化

        Args:
            node(list):
                八数码的数字，空位None
            fn_heuristic(function):启发函数，用于挑选叶子结点
        """
        self.list_node = [[1, node]]  # 存储当前的叶子节点[自己的索引,自身节点]
        self.dict_node = {1: [None, node]}  # 存储所有的节点，值为[上一节点的索引，节点]
        self.__idx = 1  # 存储的节点数
        self.shortest_path = []  # 存储最短路径
        self.fn_heuristic = fn_heuristic

    def is_exist(self, node):
        """
        判断该节点是否存在

        Args:
            node(list):
                八数码的数字，空位None
        Returns:
            (bool)存在返回True，否则为False
        """
        list_key = self.dict_node.values()
        for list_idx in list_key:
            if node == list_idx[1]:
                return True
        else:
            return False

    def up_move(self, node):
        """
        上移，根据Node的移动方向决定

        Args:
            node(list):
                八数码的数字，空位None

        Returns:
            (list) 移动后新的节点
        """
        copy_node = copy.deepcopy(node)
        idx = copy_node.index(None)
        copy_node[idx] = copy_node[idx - 3]
        copy_node[idx - 3] = None
        return copy_node

    def down_move(self, node):
        """
        下移，根据Node的移动方向决定

        Args:
            node(list):
                八数码的数字，空位None

        Returns:
            (list) 移动后新的节点
        """
        copy_node = copy.deepcopy(node)
        idx = copy_node.index(None)
        copy_node[idx] = copy_node[idx + 3]
        copy_node[idx + 3] = None
        return copy_node

    def left_move(self, node):
        """
        左移，根据Node的移动方向决定

        Args:
            node(list):
                八数码的数字，空位None

        Returns:
            (list) 移动后新的节点
        """
        copy_node = copy.deepcopy(node)
        idx = copy_node.index(None)
        copy_node[idx] = copy_node[idx - 1]
        copy_node[idx - 1] = None
        return copy_node

    def right_move(self, node):
        """
        右移，根据Node的移动方向决定

        Args:
            node(list):
                八数码的数字，空位None

        Returns:
            (list) 移动后新的节点
        """
        copy_node = copy.deepcopy(node)
        idx = copy_node.index(None)
        copy_node[idx] = copy_node[idx + 1]
        copy_node[idx + 1] = None
        return copy_node

    def create_node(self, end_node, bool_select, limit):
        """
        从叶子节点中产生新的节点

        Args:
            end_node(list):
                目标节点
            bool_select(bool):
                选择阈值的方法，True为Manhattan距离阈值，False为节点个数阈值
            limit(int):
                阈值数字

        Returns:
            (list)返回所有新产生的叶子节点的列表
        """
        temp_list_node = copy.deepcopy(self.list_node)
        self.list_node = []
        list_node = []
        for idx, node in temp_list_node:
            index = node.index(None)
            # 判断能否上移
            if index not in [0, 1, 2]:
                up_node = self.up_move(node)
                if not self.is_exist(up_node):
                    list_node.append([idx, up_node])
            # 判断能否下移
            if index not in [6, 7, 8]:
                down_node = self.down_move(node)
                if not self.is_exist(down_node):
                    list_node.append([idx, down_node])
            # 判断能否左移
            if index not in [0, 3, 6]:
                left_node = self.left_move(node)
                if not self.is_exist(left_node):
                    list_node.append([idx, left_node])
            # 判断能否右移
            if index not in [2, 5, 8]:
                right_node = self.right_move(node)
                if not self.is_exist(right_node):
                    list_node.append([idx, right_node])
        # 选择manhattan距离最短的节点
        for idx_node in list_node:
            idx_node.append(self.fn_heuristic(idx_node[1], end_node))
        # 阈值处理
        if bool_select:
            while len(self.list_node) == 0:
                for key in list_node:
                    if key[2] < limit:
                        self.__idx += 1
                        self.list_node.append([self.__idx, key[1]])
                        self.dict_node[self.__idx] = [key[0], key[1]]
                limit += 2
        else:
            sort_key = sorted(list_node, key=lambda x: x[2])
            for i in range(0, min(len(sort_key), limit)):
                self.__idx += 1
                self.list_node.append([self.__idx, sort_key[i][1]])
                self.dict_node[self.__idx] = [sort_key[i][0], sort_key[i][1]]
        return copy.deepcopy(self.list_node)

    def get_shortest_path(self, idx):
        """
        获取最短路径

        Arg:
            idx(int):
                到达目的地的索引
        """
        temp_list = []
        idx, node = self.dict_node[idx]
        # 从叶子到根节点的顺序
        temp_list.append(node)
        while idx is not None:
            idx, node = self.dict_node[idx]
            temp_list.append(node)
        self.shortest_path.append(temp_list)


def IDA_Star(start_node, end_node, bool_select, limit):
    """
    IDA*算法找出八数码的路径

    Arg:
        start_node(list):
            八数码的数字，空位None
        end_node(list):
            八数码的数字，空位None
        bool_select(bool):
                选择阈值的方法，True为Manhattan距离阈值，False为节点个数阈值
        limit(int):
            阈值数字
    """
    if start_node == end_node:
        print "开始和结束的八数码相同"
        return None
    if not is_solve(start_node, end_node):
        print "八数码无解"
        return None
    begin_node = CIDANode(start_node, calc_manh)
    list_node = begin_node.create_node(end_node, bool_select, limit)
    list_idx = []
    # 搜索操作
    while len(list_idx) == 0:
        for idx, node in list_node:
            if node == end_node:
                list_idx.append(idx)
        if len(list_idx) == 0:
            list_node = begin_node.create_node(end_node, bool_select, limit)
    # 得到路径
    for i in list_idx:
        begin_node.get_shortest_path(i)
    # 输出路径
    i = 1
    for list_path in begin_node.shortest_path:
        list_path.reverse()
        print "路径{0}：".format(i)
        print "步数：", len(list_path) - 1
        i += 1
        for node in list_path:
            print np.array(node).reshape([3, 3])
            print
