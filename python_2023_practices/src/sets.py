###
colors = {'red', 'green', 'blue', 'yellow'}

print('purple' in colors)

colors.add('purple')

print(colors)


###
numbers_list = [1, 2, 3, 4, 3, 2, 1, 5, 6, 5, 4]

unique_numbers = set(numbers_list)

print(unique_numbers)
print(len(unique_numbers))


###
flavors = {'chocolate', 'vanilla', 'strawberry'}

flavors.update({'mint', 'bubble gum'})

print(flavors)



###
tools = {
    'hammer',
    'wrench',
    'screwdriver',
    'pliers'
}

tools.remove('wrench')
tools.discard('saw')

print(tools)

###
planets = {'earth', 'jupiter', 'mars'}

planets.discard('venus')
planets.clear()

print(planets)

###
set_x = {10, 20, 30, 40, 50}
set_y = {30, 40, 50, 60, 70}
set_z = {5, 15, 25, 35}

print(set_x.union(set_y))
print(set_x | set_y)

print(set_x & set_y)
print(set_x.intersection(set_y, set_z))

print(set_y.symmetric_difference(set_z))
print(set_y ^ set_z)

print(set_y - set_x)

set_all = set_x | set_y | set_z

print(set_all)

print(set_x.isdisjoint(set_y))
print(set_x.isdisjoint(set_z))

print(set_x.issubset(set_y))
print(set_x.issubset(set_z))

print(set_x.issuperset(set_y))
print(set_y.issuperset(set_x))


# frozenset
fs = frozenset('hello')

print('h' in fs)

fs1 = frozenset([1, 2, 3])
fs2 = frozenset([2, 3, 4])
fs3 = frozenset([3, 4, 5])

print(fs1 | fs2 | fs3)


###
permissions = frozenset({
    'read',
    'write',
    'execute'
})

print('delete' in permissions)


###
frozenset_A = frozenset({1, 2, 3})
frozenset_B = frozenset({2, 3, 4})

print(frozenset_A | frozenset_B)
print(frozenset_A & frozenset_B)
print(frozenset_A - frozenset_B)


###
nodes = {
    frozenset([1, 2]): 10,
    frozenset([3, 4]): 20,
    frozenset([5, 6]): 30,
}


###