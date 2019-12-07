import intcode
import itertools

with open("input.txt", "r") as f:
    program = [int(n) for n in f.readline().split(',')]

def output_from_settings(settings, p=program):
    amp_a = intcode.Intcode(p[:], [settings[0]])
    amp_b = intcode.Intcode(p[:], [settings[1]])
    amp_c = intcode.Intcode(p[:], [settings[2]])
    amp_d = intcode.Intcode(p[:], [settings[3]])
    amp_e = intcode.Intcode(p[:], [settings[4]])

    amp_list = [amp_a,amp_b,amp_c,amp_d,amp_e]
    amp_index = 0
    current_sig = 0
    last_output = 0
    try:
        while True:
            if amp_index > 4:
                last_output = current_sig
                amp_index = 0
            current_amp = amp_list[amp_index]
            current_amp.send_input(current_sig)
            current_sig = next(current_amp)
            amp_index += 1
    except StopIteration:
        return last_output


test_prg = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
            27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
print("TEST:", output_from_settings([9,8,7,6,5], p=test_prg))

print(max(output_from_settings(settings) for settings in itertools.permutations([5,6,7,8,9])))
