
class file:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class directory:
    def __init__(self, name, parent, files=None, dirs=None):
        self.name = name
        self.parent = parent
        if files is None:
            self.files = []
        else:
            self.files = files
        if dirs is None:
            self.dirs = {}
        else:
            self.dirs = dirs

    def add_file(self, name, size):
        self.files.append(file(name, size))

    def add_dir(self, name, parent, files=None, dirs=None):
        self.dirs[name] = directory(name, parent, files, dirs)

    def total_size(self):
        total_size = 0 
        for file in self.files:
            total_size += file.size

        for dir_ in self.dirs.values():
            total_size += dir_.total_size()
        return total_size

    def print_dir(self, indent=0, indent_inc=3):
        print(' '*indent+'-', self.name, '(dir)')
        for dir_ in self.dirs.values():
            dir_.print_dir(indent+indent_inc, indent_inc)
        for file in self.files:
            print(' '*(indent+indent_inc)+'-', file.name, '(file, size='+str(file.size)+')')


if __name__ == '__main__':
    verbose = False
    f = open('input.txt', 'r')
    lines = f.readlines()

    current_dir = None
    all_dirs = []

    for line in lines:
        line = line.strip().split(' ')

        if line[1] == 'cd':
            if current_dir is None:
                home_dir = directory(name=line[2], parent=None)
                current_dir = home_dir
                all_dirs.append(current_dir)

            else:
                if line[2] == '..':
                    current_dir = current_dir.parent
                elif line[2] not in current_dir.dirs.keys():
                    exit('Trying to enter a dir that does not exist')
                else:
                    current_dir = current_dir.dirs[line[2]]
                    all_dirs.append(current_dir)
        
        elif line[0] == 'dir':
            if line[1] not in current_dir.dirs.keys():
                current_dir.add_dir(line[1], current_dir)        
                

        elif line[1] == 'ls':
            pass

        else:  # type(line[1]) == int:
            current_dir.add_file(line[1], int(line[0]))
    
    unused_space = 70000000 - home_dir.total_size()
    required_deleted = 30000000 - unused_space
    potentials = []
    total_size = 0
    for dir_ in all_dirs:
        size = dir_.total_size()
        if size <= 100000:
            total_size += size
        if size >= required_deleted:
            potentials.append(size)
    
    print('Part one:', total_size)
    print('Part two:', min(potentials))

