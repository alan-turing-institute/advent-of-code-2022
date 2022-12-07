with open("./day_06_input.txt") as f:
    signal = f.read().strip()

def check_signal(stream, characters):
    for i in range(characters, len(stream)):
        chunk = stream[i-characters:i]
        count = 0
        items = len(chunk) - 1
        for ind, x in enumerate(chunk):
            if x in chunk[-(items - ind):]:
                break
            count += 1
        if count == items:
            return(i)

print("Start of signal:", check_signal(signal, 4))
print("Start of message:", check_signal(signal, 14))
