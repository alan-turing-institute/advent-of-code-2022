def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


# keep track what cycle on and where register is
# register corresponds to middle position of sprite
cycle = 0
register = 1
# at each cycle we track where the register/sprite is
# we also track what the CRT is printing
sprite_pos = []
crt = []

lines = read_input("input10.txt")
for line in lines:
    if line == "noop":
        sprite_pos.append(register)
        if (cycle % 40) in [register-1, register, register+1]:
            crt.append("#")
        else:
            crt.append(".")
        cycle += 1
    else:
        _, num_str = line.split()
        for _ in range(2):
            sprite_pos.append(register)
            if (cycle % 40) in [register-1, register, register+1]:
                crt.append("#")
            else:
                crt.append(".")
            cycle += 1
            
        register += int(num_str)

# PART 1 ===============================================
total = 0
for n in [20, 60, 100, 140, 180, 220]:
    total += sprite_pos[n-1] * n
print(total)

# PART 2 ===============================================
for i in range(6):
    print(crt[i*40:i*40+40])