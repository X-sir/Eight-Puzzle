# coding=utf-8
"""
Author:胡立新    Version:1.0    Date:2017-5-5

Description:此模块用于解决八数码问题

Function list:
    类：CStateNode：广度优先搜索求出八数码的最短路径的基本操作

History:
"""
import copy


class CStateNode(object):
    def __init__(self, node):
        """
        对象初始化

        Args:
            node(list):
                八数码的数字，空位None
        """
        self.list_node = [[1, node]]  # 存储当前的叶子节点[自己的索引,自身节点]
        self.dict_node = {1: [None, node]}  # 存储所有的节点，值为[上一节点的索引，节点]
        self.__idx = 1  # 存储的节点数
        self.shortest_path = []  # 存储最短路径

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

    def create_node(self):
        """
        从叶子节点中产生新的节点

        Returns:
            (list)返回所有新产生的叶子节点的列表
        """
        temp_list_node = copy.deepcopy(self.list_node)
        self.list_node = []
        for idx, node in temp_list_node:
            index = node.index(None)
            # 判断能否上移
            if index not in [0, 1, 2]:
                up_node = self.up_move(node)
                if not self.is_exist(up_node):
                    self.__idx += 1
                    self.list_node.append([self.__idx, up_node])
                    self.dict_node[self.__idx] = [idx, up_node]
            # 判断能否下移
            if index not in [6, 7, 8]:
                down_node = self.down_move(node)
                if not self.is_exist(down_node):
                    self.__idx += 1
                    self.list_node.append([self.__idx, down_node])
                    self.dict_node[self.__idx] = [idx, down_node]
            # 判断能否左移
            if index not in [0, 3, 6]:
                left_node = self.left_move(node)
                if not self.is_exist(left_node):
                    self.__idx += 1
                    self.list_node.append([self.__idx, left_node])
                    self.dict_node[self.__idx] = [idx, left_node]
            # 判断能否右移
            if index not in [2, 5, 8]:
                right_node = self.right_move(node)
                if not self.is_exist(right_node):
                    self.__idx += 1
                    self.list_node.append([self.__idx, right_node])
                    self.dict_node[self.__idx] = [idx, right_node]
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
