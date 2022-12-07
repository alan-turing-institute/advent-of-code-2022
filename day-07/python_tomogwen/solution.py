
class file:
    
    def __init__(self, name, size):
        self.name = name
        self.size = size


class directory:

    def __init__(self, parent, files=None, dirs=None):
        self.parent = parent
        if files is None:
            self.files = []
        else:
            self.files = files
        if dirs is None:
            self.dirs = {}
        else:
            self.dirs = dirs

    def add_file(name, size):
        self.files.append(file(name, size))

    
    def add_dir(name, parent, files=None, dirs=None):
        self.dirs[name] = directory(parent, files, dirs)


    def total_size(self):
        total_size = 0 
        for file in files:
            total_size += file.size

        for dir_ in dirs:
            total_size += dir_.total_size()

        return total_size


def get_line(lines, line_pos):
    line = lines[line_pos].strip().split(' ')
    print(line_pos, line)    
    line_pos += 1
    return line, line_pos


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    line_pos = 0
    current_dir = None
    line, line_pos = get_line(lines, line_pos)
    
    while line_pos < len(lines):
        if line[0] != '$':
            exit('Should start loop at command')

        if line[1] == 'cd':
            if current_dir is None:
                home_dir = directory(parent=None)
                current_dir = home_dir
                line, line_pos = get_line(lines, line_pos)
            else:
                if line[2] not in current_dir.dirs.keys():
                    exit('Trying to enter a dir that does not exist')
                else:
                    current_dir = current_dir.dirs[line[2]]
                    line, line_pos = get_line(lines, line_pos)

        if line[1] == 'ls':
            line, line_pos = get_line(lines, line_pos)
            while line[0] != '$':
                if type(line[1]) == int:
                    current_dir.add_file(line[2], line[1])
                    line, line_pos = get_line(lines, line_pos)
                if line[1] == 'dir':
                    print('in dir')
                    current_dir.add_dir(name=line[2], parent=current_dir)
                    line, line_pos = get_line(lines_, line_pos)
    
    print(home_dir.total_size())




