# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 19:22:33 2021

@author: Chutj
"""

import genetic
import unittest
import datetime
from libpysal.weights import Queen

shapefile_path = "G:/Python_Home1/stl_hom_utm.shp"

weights = Queen.from_shapefile(shapefile_path, "POLY_ID_OG")
one_neighbor_other = weights.neighbors


# 定义“规则”，用以将区域之间的空间连接情况转换为遗传算法可以识别的信息。被“规则”连接的两个区域在空间中是相邻的

class Rule:
    Item = None
    Other = None
    Stringified = None

    def __init__(self, item, other, stringified):
        self.Item = item
        self.Other = other
        self.Stringified = stringified

    def __eq__(self, another):
        return hasattr(another, 'Item') and \
               hasattr(another, 'Other') and \
               self.Item == another.Item and \
               self.Other == another.Other

    def __hash__(self):
        return hash(self.Item) * 397 ^ hash(self.Other)

    def __str__(self):
        return self.Stringified


# 定义区域空间连接情况检查所需函数，用以确保区域两两之间相邻情况的准确

def buildLookup(items):
    itemToIndex = {}
    index = 0
    for key in sorted(items):
        itemToIndex[key] = index
        index += 1
    return itemToIndex


def buildRules(items):
    itemToIndex = buildLookup(items.keys())
    rulesAdded = {}
    rules = []
    keys = sorted(list(items.keys()))

    for key in sorted(items.keys()):
        keyIndex = itemToIndex[key]
        adjacentKeys = items[key]
        for adjacentKey in adjacentKeys:
            if adjacentKey == '':
                continue
            adjacentIndex = itemToIndex[adjacentKey]
            temp = keyIndex
            if adjacentIndex < temp:
                temp, adjacentIndex = adjacentIndex, temp
            ruleKey = str(keys[temp]) + "->" + str(keys[adjacentIndex])
            rule = Rule(temp, adjacentIndex, ruleKey)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1
                rules.append(rule)

    for k, v in rulesAdded.items():
        if v == 1:
            print("rule %s is not bidirectional" % k)

    return rules


# 定义颜色所代表的基因组

colors = ["Orange", "Yellow", "Green", "Blue"]
colorLookup = {}
for color in colors:
    colorLookup[color[0]] = color
geneset = list(colorLookup.keys())


# 定义个体基因型，其中各个体有78个基因，每一个基因代表一个区域。个体基因需要满足“规则”中相邻的区域具有不同的颜色

class GraphColoringTests(unittest.TestCase):
    def test(self):
        rules = buildRules(one_neighbor_other)
        colors = ["Orange", "Yellow", "Green", "Blue"]
        colorLookup = {}
        for color in colors:
            colorLookup[color[0]] = color
        geneset = list(colorLookup.keys())
        optimalValue = len(rules)
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, rules)
        best = genetic.getBest(fnGetFitness, fnDisplay, len(one_neighbor_other), optimalValue, geneset)
        self.assertEqual(best.Fitness, optimalValue)

        keys = sorted(one_neighbor_other.keys())

        for index in range(len(one_neighbor_other)):
            print(keys[index], " is ", colorLookup[best.Genes[index]])


# 输出各区域颜色

def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


# 检查各区域颜色是否与个体基因所代表的颜色一致

def getFitness(candidate, rules):
    rulesThatPass = 0
    for rule in rules:
        if candidate[rule.Item] != candidate[rule.Other]:
            rulesThatPass += 1

    return rulesThatPass


# 运行程序

GraphColoringTests().test()
