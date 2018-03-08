import re
class QuarterstaffInterpreter:
    def __init__(self, program):
        self.input = None
        self.input_index = 0
        self.eof = False
        self.run(self.parse(program), {}, 0)
    def parse(self, program_string):
        char_index=0
        brackets_dict ={"{":"}","[":"]","(":")"}

        parsed_prog = []
        while char_index < len(program_string):
            step = 1
            if program_string[char_index].isnumeric():
                end=re.search("[^0-9]",program_string[char_index:])
                if end is None:
                    number = program_string[char_index:]
                    step = len(program_string)-char_index
                else:
                    number = program_string[char_index:][:end.start()]
                    step = end.start()
                parsed_prog.append((0,int(number)))
            elif program_string[char_index].isalpha():
                end=re.search("[^A-Za-z]",program_string[char_index:])
                if end is None:
                    variable = program_string[char_index:]
                    step = len(program_string)-char_index
                else:
                    variable = program_string[char_index:][:end.start()]
                    step = end.start()
                parsed_prog.append((1,variable))
            elif program_string[char_index] == ">":
                if not program_string[char_index+1].isalpha():
                    raise Exception
                end=re.search("[^A-Za-z]",program_string[char_index+1:])
                if end is None:
                    variable = program_string[char_index+1:]
                    step = len(program_string)-char_index
                else:
                    variable = program_string[char_index+1:][:end.start()]
                    step = end.start()+1
                parsed_prog.append((2,variable))
            elif program_string[char_index] == "-":
                parsed_prog.append(-1)
            elif program_string[char_index] == ".":
                parsed_prog.append(0)
            elif program_string[char_index] == "?":
                parsed_prog.append(1)
            elif program_string[char_index] == "!":
                parsed_prog.append(2)
            elif program_string[char_index] in brackets_dict:
                char_offset=0
                if program_string[char_index]=="(":
                    midpoint=-1
                else:
                    midpoint=None
                scope = 1
                while scope > 0:
                    char_offset+=1
                    if program_string[char_index+char_offset] in brackets_dict:
                        scope += 1
                    elif program_string[char_index+char_offset] in brackets_dict.values():
                        scope -= 1
                    elif scope == 1 and program_string[char_index+char_offset] == "|":
                        midpoint = char_offset
                if program_string[char_index+char_offset] != brackets_dict[program_string[char_index]]:
                    raise Exception
                else:
                    if midpoint == None:
                        parsed_prog.append((3+"[{(".find(program_string[char_index]),
                                        self.parse(program_string[char_index+1:][:char_offset-1])))
                    else:
                        if midpoint == -1:
                             parsed_prog.append((3+"[{(".find(program_string[char_index]),
                                self.parse(program_string[char_index+1:][:char_offset-1])))
                        else:
                            parsed_prog.append((3+"[{(".find(program_string[char_index]),
                                self.parse(program_string[char_index+1:][:midpoint-1]),
                                self.parse(program_string[char_index+1+midpoint:char_index+char_offset])))

                step = char_offset+1
            elif program_string[char_index] == "|" or program_string[char_index] in brackets_dict.values():
                raise Exception
            char_index += step
        return tuple(parsed_prog)



    def run(self,program, var_dict, value):
        for i in program:
            if type(i) is int:
                if i == -1:  # -
                    value *= -1
                elif i == 0: # .
                    value = 0
                elif i == 1: # ?
                    if not self.eof:
                        if self.input is None:
                            try:
                                self.input = input()
                            except EOFError:
                                self.eof= True
                                self.input = chr(0)

                        if self.input_index==len(self.input):
                            self.input_index = 0
                            self.input = None
                            value += 10  # ord("\n")
                        else:
                            value += ord(self.input[self.input_index])
                            self.input_index += 1
                elif i == 2: # !
                    print(chr(value),end="")
                    value = 0
            else: # type(i) is tuple or whatever
                if i[0] == 0:
                    value += i[1]
                elif i[0] == 1:
                    if i[1] in var_dict:
                        value += var_dict[i[1]]
                elif i[0] == 2:
                    var_dict[i[1]] = value
                    value = 0
                elif i[0] >= 3:
                    if i[0] == 3:
                        while value:
                            var_dict, value = self.run(i[1],var_dict,value)
                    elif i[0] == 4:
                        while not value:
                            var_dict, value = self.run(i[1],var_dict,value)
                    elif i[0] == 5:
                        if value:
                            var_dict, value = self.run(i[1],var_dict,value)
                        elif len(i) == 3:
                            var_dict, value = self.run(i[2],var_dict,value)
        return var_dict, value
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interpret the Quarterstaff language")
    parser.add_argument("program", metavar="program", type=str, help="path to the program")
    QuarterstaffInterpreter(open(parser.parse_args().program).read())