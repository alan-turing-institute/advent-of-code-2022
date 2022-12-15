def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def check_order(left_list, right_list):
    """
    Recursively compare two lists (of lists and ints).
    """

    for l,r in zip(left_list, right_list):
        # if both are ints and not the same value, can stop
        if isinstance(l,int) and isinstance(r,int):    
            if l < r:
                return True
            if l > r:
                return False
        else:
            # compare items in lists
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            check = check_order(l, r)
            if check is not None:
                return check
    # if lists are not same length, can stop
    if len(left_list) > len(right_list):
        return False
    if len(left_list) < len(right_list):
        return True


# PARSE INPUT
lines = read_input("input13.txt")
packets = [eval(line) for line in lines if line != ""]


# PART 1: check if packet pairs are correctly ordered
# return sum of indices of correctly ordered packets
total_1 = 0
for i in range(len(packets)//2):
    left, right = packets[i*2:i*2+2] 
    if check_order(left, right):
        total_1 += (i+1)

print("part 1:", total_1)


# PART 2: determine correct order of packets
# return indices of divired packets once orderd
divider_packets = [[[2]], [[6]]]
packets.extend(divider_packets)

# use inbuilt python sort
class Packet:
    def __init__(self, packet):
        self.packet = packet
    def __lt__(self, packet2):
        """Less than method"""
        return check_order(self.packet, packet2.packet)

class_packets = [Packet(vals) for vals in packets]
class_packets.sort()

total_2 = 1
for i, packet in enumerate(class_packets):
    if packet.packet in divider_packets:
        total_2 *= (i+1)

print("part 2:", total_2)