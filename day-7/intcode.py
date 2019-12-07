class Intcode:
    def __init__(self, data, d_in=None):
        self.data = data
        self.d_in = list(d_in) or []
        self.i = 0
    def send_input(self, new_input):
        self.d_in.append(new_input)
    def __next__(self):
        while True:
            op = self.data[self.i]
            modes = [(op//100) % 10, (op//1000) % 10, (op//10000) % 10]
            opcode = op % 100
            if opcode == 1:
                self.data[self.get_raw_c()] = self.get_arg_a(modes) + self.get_arg_b(modes)
                self.i += 4
            elif opcode == 2:
                self.data[self.get_raw_c()] = self.get_arg_a(modes) * self.get_arg_b(modes)
                self.i += 4
            elif opcode == 3:
                self.data[self.get_raw_a()] = self.d_in.pop(0)
                self.i += 2
            elif opcode == 4:
                r = self.get_arg_a(modes)
                self.i += 2
                return r
            elif opcode == 5:
                if self.get_arg_a(modes) != 0:
                    self.i = self.get_arg_b(modes)
                else:
                    self.i += 3
            elif opcode == 6:
                if self.get_arg_a(modes) == 0:
                    self.i = self.get_arg_b(modes)
                else:
                    self.i += 3
            elif opcode == 7:
                if self.get_arg_a(modes) < self.get_arg_b(modes):
                    self.data[self.get_raw_c()] = 1
                else:
                    self.data[self.get_raw_c()] = 0
                self.i += 4
            elif opcode == 8:
                if self.get_arg_a(modes) == self.get_arg_b(modes):
                    self.data[self.get_raw_c()] = 1
                else:
                    self.data[self.get_raw_c()] = 0
                self.i += 4
            elif opcode == 99:
                raise StopIteration
            else:
                raise ValueError("Invalid opcode "+str(op))

    def get_arg_a(self, modes):
        ai = self.i+1
        return self.data[ai] if modes[0] == 1 else self.data[self.data[ai]] if modes[0] == 0 else None

    def get_raw_a(self):
        return self.data[self.i+1]

    def get_arg_b(self, modes):
        bi = self.i+2
        return self.data[bi] if modes[1] == 1 else self.data[self.data[bi]] if modes[1] == 0 else None

    def get_raw_b(self):
        return self.data[self.i+2]

    def get_arg_c(self, modes):
        ci = self.i+3
        return self.data[ci] if modes[2] == 1 else self.data[self.data[ci]] if modes[2] == 0 else None

    def get_raw_c(self):
        return self.data[self.i+3]
