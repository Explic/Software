import pick
from pick import pick

options = ["[EXIT]", "[RETURN]", "test", 'test2']
option, index = pick(options, "Title", indicator='=>', default_index=0)

print(option)
