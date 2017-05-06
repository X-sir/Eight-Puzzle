# coding=utf-8
"""
Author:胡立新    Version:1.0    Date:2017-5-5

Description:广度优先搜索、双向广度优先搜索解决八数码问题。
            有无解的判断：
            一个状态表示成一维的形式，求出除0之外所有数字的逆序数之和，也就是每个数字前面比它大的
            数字的个数的和，称为这个状态的逆序。若两个状态的逆序奇偶性 相同，则可相互到达，否则不
            可相互到达。

Function list:
        bfs:广度优先搜索解决八数码问题

History:
"""

from CStateNode import CStateNode
import numpy as np
import time
import copy


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


def bfs(start_node, end_node):
    """
    广度优先搜索求解八数码问题

    Arg:
        start_node(list):
            八数码的数字，空位None
        end_node(list):
            八数码的数字，空位None
    """
    if start_node == end_node:
        print "开始和结束的八数码相同"
        return None
    if not is_solve(start_node, end_node):
        print "八数码无解"
        return None
    begin_node = CStateNode(start_node)
    list_node = begin_node.create_node()
    list_idx = []
    # 搜索操作
    while len(list_idx) == 0:
        for idx, node in list_node:
            if node == end_node:
                list_idx.append(idx)
        if len(list_idx) == 0:
            list_node = begin_node.create_node()
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


def double_bfs(start_node, end_node):
    """
        双向广度优先搜索求解八数码问题

        Arg:
            start_node(list):
                八数码的数字，空位None
            end_node(list):
                八数码的数字，空位None
    """
    if start_node == end_node:
        print "开始和结束的八数码相同"
        return None
    if not is_solve(start_node, end_node):
        print "八数码无解"
        return None
    begin_node = CStateNode(start_node)
    over_node = CStateNode(end_node)
    list_node1 = begin_node.create_node()
    list_node2 = over_node.list_node
    list_idx1 = []
    list_idx2 = []
    # 双向搜索操作
    i = 1
    while len(list_idx1) == 0:
        for idx1, node1 in list_node1:
            for idx2, node2 in list_node2:
                if node2 == node1:
                    list_idx1.append(idx1)
                    list_idx2.append(idx2)
        if len(list_idx1) == 0:
            if i % 2 == 0:
                list_node1 = begin_node.create_node()
            else:
                list_node2 = over_node.create_node()
            i += 1
    # 得到路径
    for i in range(len(list_idx1)):
        begin_node.get_shortest_path(list_idx1[i])
        over_node.get_shortest_path(list_idx2[i])
    # 输出路径
    i = 1
    for idx in range(len(begin_node.shortest_path)):
        begin_node.shortest_path[idx].reverse()
        print "路径{0}：".format(i)
        print "步数：", len(begin_node.shortest_path[idx]) + len(over_node.shortest_path[idx]) - 2
        i += 1
        for node in begin_node.shortest_path[idx]:
            print np.array(node).reshape([3, 3])
            print
        over_node.shortest_path[idx].pop(0)
        for node in over_node.shortest_path[idx]:
            print np.array(node).reshape([3, 3])
            print


if __name__ == "__main__":
    list_start = [2, 8, 3, 1, None, 4, 7, 6, 5]
    list_end = [1, 6, 2, None, 3, 4, 8, 7, 5]
    start_time = time.clock()
    bfs(list_start, list_end)
    end_time = time.clock()
    print "广度优先搜索的时间：", end_time - start_time
    # start_time = time.clock()
    # double_bfs(list_start, list_end)
    # end_time = time.clock()
    # print "双向广度优先搜索的时间：", end_time - start_time
