# http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
"""
G = {'s':{'u':10, 'x':5},
     'u':{'v':1, 'x':2},
     'v':{'y':4},
     'x':{'u':3, 'v':9, 'y':2},
     'y':{'s':7, 'v':6}}
"""
def graph_to_dot(G):
    s = """digraph G {\nnode [width=.3,height=.3,shape=octagon,style=filled,color=skyblue];\noverlap="false";\nrankdir="LR";\n%s}"""
    r = ''
    for i in G:
        for j in G[i]:
            r+='%s -> %s [label="%s"];\n' % (i, j, str(G[i][j])) 
    return s % (r)

# http://graphviz-dev.appspot.com/
# http://ashitani.jp/gv/#