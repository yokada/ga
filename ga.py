import random
from pprint import pprint

def init(population_size, node_size):
	inds = []
	i = 0
	while i < population_size:
		t = gen_ind(node_size)
		if i == 0:
			inds.append(t)
			i+=1
			continue
		elif i >= population_size:
			break
		for e in inds:
			if e != t:
				inds.append(t)
				i+=1
				break
	return inds

def gen_ind(node_size):
	nodes = node_list(node_size)
	random.shuffle(nodes)
	return nodes

def node_list(node_size):
	return range(1, node_size+1)

def to_genotype(p):
	nodes = node_list(len(p))
	ret = []
	while len(p) > 0:
		v = p.pop(0)
		d = nodes.index(v)
		ret.append(d)
		nodes.remove(v)
	return ret


# geno type:  0, 3, 0, 1, 0
# pheno type: 1, 5, 2, 4, 3
# 0 3 0 1 0

# 0
# 0 1 2 3 4 => 1
# 1 2 3 4 5

# 3
# 0 1 2 3 4 => 5
# 2 3 4 5

# 0
# 0 1 2 3 4 => 2
# 2 3 4

# 1
# 0 1 2 3 4 => 4
# 3 4

# 0
# 0 1 2 3 4 => 3
# 3

def to_phenotype(g):
	ret = []
	nodes = node_list(len(g))
	ret = []
	while len(g) > 0:
		i = g.pop(0)
		d = nodes.pop(i)
		ret.append(d)
	return ret

def evaluate(inds, costs):
	totals = []
	for ind in inds:
		i = 0
		t = 0
		while i<(len(ind)-1):
			t += costs[ind[i]-1][ind[i+1]-1];
			i += 1
		totals.append(t)
	return totals

def evaluate_again(geno_children, costs):
	pheno_inds = []
	for g in geno_children:
		p = to_phenotype(g)
		pheno_inds.append(p)

	return evaluate(pheno_inds, costs)

# return parents as array
def select_with_roolet(inds, scores):
	probs = []
	amount = sum(scores)
	for s in scores:
		probs.append( round(s / float(amount), 3) * 1000 )

	parents = []
	while len(parents) < 2:
		realm = 0
		determining = round(random.uniform(1, 1000))
		for p in probs:
			realm += p
			if realm >= determining:
				parents.append( inds[probs.index(p)] )
				break

	return parents


def crossover(parents):
	first = list( parents[0] )
	second = list( parents[1] )

	geno_first = to_genotype( first )
	geno_second = to_genotype( second )

	children = []

	while len(children) < 3:
		my_filter = bin( random.randint(0, 31) ).replace('0b', '').zfill(5)
		i = 0
		for c in my_filter:
			if c == '0':
				i+=1
				continue
			tmp = geno_first[i]
			#pprint("i:%d" % i)
			geno_first[i] = geno_second[i]
			geno_second[i] = tmp
		children.append(geno_first)
		if len(children) < 3:
			children.append(geno_second)

	return children

def mutate(children, prob):
	mutated_children = []
	count = sum( [len(c) for c in children] )
	realm = prob * 100
	mutated = False
	for c in children:
		child = []
		for e in c:
			determining = round(random.uniform(1, 100))
			if determining <= realm and mutated == False:
				# do mutation!
				child.append(0)
				mutated = True
			else:
				child.append(e)
		mutated_children.append(to_phenotype(child))
	return mutated_children

max_cycle = 100
node_size = 5
population_size = 3
# solving space
# [2,1,3,5,4]
# => [2, 1], [1, 3], [3, 5], [5, 4]
# => consts[1][0], consts[0][2], ...
costs = [
	[0, 1, 2, 3, 4],
	[1, 0, 3, 4, 1],
	[4, 3, 0, 1, 5],
	[5, 4, 1, 0, 1],
	[5, 1, 4, 1, 0],
]

inds = init(population_size, node_size)
pprint(inds)
scores = evaluate(inds, costs)
pprint(sum(scores))

i = 0
while True:
	parents = select_with_roolet(inds, scores)
	children = crossover(parents)
	inds = mutate(children, 0.05)
	i+=1

	if i >= max_cycle:
		scores = evaluate(inds, costs)
		break

pprint(sum(scores))
