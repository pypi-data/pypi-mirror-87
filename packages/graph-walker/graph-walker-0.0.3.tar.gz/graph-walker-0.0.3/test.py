import networkx as nx
import walker

# create a random graph
G = nx.random_partition_graph([1000] * 15, .01, .001)

# generate random walks
X = walker.random_walks(G, n_walks=50, walk_len=25)

# generate random walks according to Node2Vec methodology
X = walker.node2vec_random_walks(G, n_walks=50, walk_len=25, p=.25, q=.25)

# corrupt random walks by randomly changing nodes in random walks
X, y = walker.corrupt(G, X, r=.1)
