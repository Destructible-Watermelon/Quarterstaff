class QuarterBFInterpreter:
    def __init__(self, program):
        import re
        program = re.sub(r"[^+\-<>.,\[\]]", "", program)
        self.input = None
        self.input_index = 0
        self.eof = False
        self.run(self.parse(program), [0], 0)
    def parse(self, program_string):
        i=0
        parsed_prog = []
        while i < len(program_string):
            if program_string[i] == ",":
                parsed_prog.append(0)
                i += 1
            elif program_string[i] == ".":
                parsed_prog.append(1)
                i += 1
            elif program_string[i] in "+-><":
                effects = {}
                offset = 0
                while i < len(program_string) and program_string[i] not in "[].,":
                    if program_string[i] == "+":
                        if offset in effects:
                            effects[offset] += 1
                        else:
                            effects[offset] = 1
                    elif program_string[i] == "-":
                        if offset in effects:
                            effects[offset] -= 1
                        else:
                            effects[offset] = -1
                    elif program_string[i] == ">":
                        offset += 1
                    elif program_string[i] == "<":
                        offset -= 1
                    i += 1
                for j in effects:
                    effects[j]%=256
                parsed_prog.append((0,)+ tuple(effects.items()) + (offset,))

            elif program_string[i] == "[":
                loop_start = i+1
                scope = 1
                while scope > 0:
                    i+=1
                    if program_string[i] == "[":
                        scope += 1
                    elif program_string[i] == "]":
                        scope -= 1
                parsed_prog.append((1,) + self.parse(program_string[loop_start:i]))
                i += 1
        return tuple(parsed_prog)

    def run(self, program, tape, tape_pointer):
        for i in program:
            if i == 0:
                if self.eof:
                    tape[tape_pointer]=0
                else:
                    if self.input is None:
                        try:
                            self.input = input()
                        except EOFError:
                            self.eof= True
                            self.input = chr(0)

                    if self.input_index==len(self.input):
                        self.input_index = 0
                        self.input = None
                        tape[tape_pointer] = ord("\n") #10
                    else:
                        tape[tape_pointer] =  ord(self.input[self.input_index])
                        self.input_index += 1

            elif i == 1:
                print(chr(tape[tape_pointer]),end = "")
            elif i[0] == 0:
                for cell_change in i[1:-1]:
                    cells_from_right = (len(tape)-(tape_pointer + 1))
                    if cell_change[0] > cells_from_right:
                        tape.extend([0]*(cell_change[0]-cells_from_right))
                    if tape_pointer+cell_change[0]<0:
                        raise Exception
                    tape[tape_pointer+cell_change[0]] += cell_change[1]
                    if tape[tape_pointer+cell_change[0]] >= 256:
                        tape[tape_pointer+cell_change[0]]-=256
                tape_pointer += i[-1]
                if tape_pointer >= len(tape):
                    tape.extend([0]*(tape_pointer-len(tape)+1))
                if tape_pointer < 0:
                        raise Exception
            elif i[0] == 1:
                while tape[tape_pointer]:
                    tape, tape_pointer = self.run(i[1:], tape, tape_pointer)

        return tape, tape_pointer




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interpret the QuarterBF language")
    parser.add_argument("program", metavar="program", type=str, help="path to the program")
    QuarterBFInterpreter(open(parser.parse_args().program).read())


