blogs = [
['appel watch', 'appel watch is sick', '#appel', 0],
['samsong watch', 'appel watch is sick', '#samsong', 0],
['fitness watch', 'fitness watch is sick', '#fitness #tracker', 0],
['top 10 appel watches', 'asdda', '#top #best #appel'],
['top 10 fitness trackers', 'dasdsd', '#top #best #fitness #tracker']
]

content = 'fitness'

def get_related_blogs(search):
    ranking_blogs = []
    sorting_list = []
    for b in blogs:
        ranking_value = 0
        # ranking pased on tages
        # print(blogs.index(b), 'index')
        tages = b[2]
        tages = tages.split('#')
        # print(search.split(' '))
        # print(tages, 'tages')
        for mult, word in enumerate(search.split(' ')):
            # print(word)
            for tag in tages:
                # print(tag, 'tag')
                if word != 'watch':
                    for idx, litter in enumerate(word):
                        if  idx == tag.find(litter):
                            ranking_value += 5

        # ranking pased on title
        title = b[0]
        # print(title,'title')
        for word in search.split(' '):
            if word in title:
                ranking_value += 1


        sorting_list.append((blogs.index(b), ranking_value))
        # print(ranking_value, 'RV')

    # sorting
    largest_RV = 0
    for l in sorting_list:
        if l[1] > largest_RV:
            largest_RV = l[1]
    sorting_RV = 0

    while True:
        if sorting_RV > largest_RV:
            break
        # print(sorting_RV)
        for t in sorting_list:
            if t[1] == sorting_RV:
                sorting_list.pop(sorting_list.index(t))
                sorting_list.insert(0, t)

        sorting_RV += 1
    print(sorting_list)
    # for b in sorting_list:
    #     ranking_blogs.insert(0, b)
    # print(ranking_blogs)




get_related_blogs(content.lower())

