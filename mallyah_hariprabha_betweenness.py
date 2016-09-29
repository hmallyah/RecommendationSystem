import os
import sys
import copy


temp1 = []
temp2 = []
graph = []
nodes = []
node_type = ""

with open(sys.argv[1]) as inputGraph:
    for line in inputGraph:
        temp1.append(line.strip('\n').replace(' ', ',').split(','))

if temp1[0][0].isdigit():
    node_type = "int"
    for edge in temp1:
        temp2.append(map(int, edge))

    for e in temp2:
            for n in e:
                if n not in nodes:
                    nodes.append(n)
    for edge in temp2:
         graph.append(sorted(edge))
else:
    node_type = "char"
    for e in temp1:
            for n in e:
                if n not in nodes:
                    nodes.append(n)
    for edge in temp1:
        graph.append(sorted(edge))

def BFS(graph, root, nodes):
    discovered = {}
    L = {}
    remainder = []
    for n in nodes:
        discovered[n] = False

    discovered[root] = True
    L[0] = [root]
    i = 0
    T = []
    while L[i] != []:
        L[i+1] = []
        for node in L[i]:
            incident_edges = []
            for edge in graph:
                if node in edge:
                    incident_edges.append(edge)
            for edge in incident_edges:
                for n in edge:
                    if n != node:
                        v = n
                if discovered[v] == False:
                    discovered[v] = True
                    T.append(edge)
                    L[i+1].append(v)
        i += 1
    else:
        del L[i]

    for edge in graph:
        if edge not in T:
            remainder.append(edge)

    for edge in remainder:
        level_node1 = 0
        level_node2 = 0
        for l1 in range(len(L)):
            if edge[0] in L[l1]:
                level_node1 = l1
        for l2 in range(len(L)):
            if edge[1] in L[l2] :
                level_node2 = l2

        if abs(level_node1 - level_node2) == 1:
            T.append(edge)

    return [L, T]

def girvan_newman(graph, nodes):
    betweenness = {}
    for edge in graph:
        betweenness[tuple(edge)] = 0.0
    for n in nodes:
        no_of_shortest_path = {}
        edge_credit = {}
        node_credit = {}
        bfs_result = BFS(graph, n, nodes)
        bfs_tree = bfs_result[1]
        bfs_levels = bfs_result[0]
        for level in bfs_levels:
            for node in bfs_levels[level]:
                no_of_shortest_path[node] = level
        for edge in bfs_tree:
            edge_credit[tuple(edge)] = 0.0
        for node in nodes:
            node_credit[node] = 0.0

        level = len(bfs_levels)-1
        while level != -1:
            if level == len(bfs_levels)-1:
                for node in bfs_levels[level]:
                        node_credit[node] = 1.0

            else:
                for node in bfs_levels[level]:
                    outgoing_edges = []
                    for edge in bfs_tree:
                        if edge_credit[tuple(edge)] != 0.0 and node in edge:
                            outgoing_edges.append(edge)
                    sum = 0.0
                    if outgoing_edges != []:
                        for edge in outgoing_edges:
                            sum += edge_credit[tuple(edge)]
                        node_credit[node] = 1.0 + sum
                    else:
                        node_credit[node] = 1.0

            for node in bfs_levels[level]:
                incoming_edges = []
                for edge in bfs_tree:
                    if edge_credit[tuple(edge)] == 0.0 and node in edge:
                        incoming_edges.append(edge)
                if incoming_edges != []:
                    for edge in incoming_edges:
                        for n in edge:
                            if n == node:
                                v = n
                        edge_credit[tuple(edge)] = float(node_credit[node]/len(incoming_edges))

            level -= 1
        for edge in edge_credit:
                betweenness[tuple(edge)] += edge_credit[tuple(edge)]

    for edge in betweenness:
        betweenness[edge] = float(betweenness[edge]/2)

    for edge in sorted(betweenness):
        if node_type == "int":
            print str(list(edge)) + ": " + str(betweenness[edge])
        else:
            print "[" + str(list(edge)[0]) + ", " + str(list(edge)[1]) + "]: " + str(betweenness[edge])

girvan_newman(graph, nodes)
