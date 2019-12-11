class Intcode:
    def __init__(self, data, d_in=None, *, debug=False):
        self.data = data
        self.d_in = [] if d_in is None else list(d_in)
        self.i = 0
        self.r = 0
        self.debug = debug

    def send_input(self, new_input):
        self.d_in.append(new_input)

    def set_data(self, i, v):
        if i >= len(self.data):
            self.data.extend([0 for _ in range(i-len(self.data)+1)])
        self.data[i] = v

    def get_data(self, i):
        if i >= len(self.data):
            self.data.extend([0 for _ in range(i-len(self.data)+1)])
        return self.data[i]

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            op = self.data[self.i]
            if self.debug:
                print("[{}]: {}".format(self.i, op))
            modes = [(op//100) % 10, (op//1000) % 10, (op//10000) % 10]
            opcode = op % 100
            if opcode == 1:
                self.set_data(self.get_target_c(modes), self.get_arg_a(
                    modes) + self.get_arg_b(modes))
                self.i += 4
            elif opcode == 2:
                self.set_data(self.get_target_c(modes), self.get_arg_a(
                    modes) * self.get_arg_b(modes))
                self.i += 4
            elif opcode == 3:
                self.set_data(self.get_target_a(modes), self.d_in.pop(0))
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
                    self.set_data(self.get_target_c(modes), 1)
                else:
                    self.set_data(self.get_target_c(modes), 0)
                self.i += 4
            elif opcode == 8:
                if self.get_arg_a(modes) == self.get_arg_b(modes):
                    self.set_data(self.get_target_c(modes), 1)
                else:
                    self.set_data(self.get_target_c(modes), 0)
                self.i += 4
            elif opcode == 9:
                a = self.get_arg_a(modes)
                self.r += a
                self.i += 2
                if self.debug:
                    print("R:", self.r)
            elif opcode == 99:
                raise StopIteration
            else:
                raise ValueError("Invalid opcode "+str(op))

    def get_arg_a(self, modes):
        ai = self.i+1
        r = self.get_data(ai) if modes[0] == 1 else \
            self.get_data(self.get_data(ai)) if modes[0] == 0 else \
            self.get_data(self.r + self.get_data(ai)
                          ) if modes[0] == 2 else None
        if self.debug:
            print("A:", r, "({})".format(self.get_data(ai)))
        return r

    def get_raw_a(self):
        r = self.get_data(self.i+1)
        if self.debug:
            print("A:", r)
        return r

    def get_target_a(self, modes):
        ai = self.i + 1
        r = self.get_data(ai) if modes[0] == 0 else \
            self.r + self.get_data(ai) if modes[0] == 2 else None
        if self.debug:
            print("A:", r, "({})".format(self.get_data(ai)))
        return r

    def get_arg_b(self, modes):
        bi = self.i+2
        r = self.get_data(bi) if modes[1] == 1 else \
            self.get_data(self.get_data(bi)) if modes[1] == 0 else \
            self.get_data(self.r + self.get_data(bi)
                          ) if modes[1] == 2 else None
        if self.debug:
            print("B:", r, "({})".format(self.get_data(bi)))
        return r

    def get_raw_b(self):
        r = self.get_data(self.i+2)
        if self.debug:
            print("B:", r)
        return r

    def get_target_b(self, modes):
        bi = self.i + 2
        r = self.get_data(bi) if modes[1] == 0 else \
            self.r + self.get_data(bi) if modes[1] == 2 else None
        if self.debug:
            print("B:", r, "({})".format(self.get_data(bi)))
        return r

    def get_arg_c(self, modes):
        ci = self.i+3
        r = self.get_data(ci) if modes[2] == 1 else \
            self.get_data(self.get_data(ci)) if modes[2] == 0 else \
            self.get_data(self.r + self.get_data(ci)
                          ) if modes[2] == 2 else None
        if self.debug:
            print("C:", r, "({})".format(self.get_data(ci)))
        return r

    def get_raw_c(self):
        r = self.get_data(self.i+3)
        if self.debug:
            print("C:", r)
        return r

    def get_target_c(self, modes):
        ci = self.i + 3
        r = self.get_data(ci) if modes[2] == 0 else \
            self.r + self.get_data(ci) if modes[2] == 2 else None
        if self.debug:
            print("C:", r, "({})".format(self.get_data(ci)))
        return r
