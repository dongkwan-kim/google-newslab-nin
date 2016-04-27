# class_prore

class Logic_t():
    
    def __init__(self, l_file_name):
        self.score_board = []
        for line in open(l_file_name, "r"):
            if "#" in line:
                continue
            line_arr = line.split("\t")
            if len(line_arr) == 1:
                self.max_choice = int(line_arr[0])
            else:
                from_int = int(line_arr[0])
                to_int = int(line_arr[1])
                self.score_board.append((from_int, to_int))
    
    def get_result_idx(self, score):
        for scr in self.score_board:
            if (scr[0] <= score) and (score <= scr[1]):
                return self.score_board.index(scr)
        return -1
    
    def get_max_choice(self):
        return self.max_choice

class ProblemSet_t():

    def __init__(self, p_file_name):
        self.problem_list = []
        for line in open(p_file_name, "r"):
            if "#" in line:
                continue
            new_problem = Problem(line)
            self.problem_list.append(new_problem)

    def get_len(self):
        return len(self.problem_list)
    
    def get_problem(self, idx):
        return self.problem_list[idx]

class Problem():
    
    def __init__(self, p_line):
        # idx \t problem \t explain \t choice1 \t choice2 ...
        p_arr = p_line.split("\t")
        self.idx = p_arr[0]
        self.problem_str = p_arr[1]
        self.explain_str = p_arr[2]
        self.choice_list = [x for x in p_arr[3:]]
        # print(dict([(x_idx, p_arr[2+x_idx]) for x_idx in range(len(p_arr[3:]))]))

    def get_idx_str(self):
        return str(self.idx)
    
    def get_problem(self):
        return self.problem_str

    def get_explain(self):
        return self.explain_str

    def get_choice_list(self):
        return self.choice_list

class ResultSet_t():

    def __init__(self, r_file_name):
        self.result_list = []
        for line in open(r_file_name, "r"):
            if "#" in line:
                continue
            new_result = Result(line)
            self.result_list.append(new_result)

    def get_result(self, idx):
        return self.result_list[idx]


class Result():

    def __init__(self, r_line):
        # idx \t result \t explain
        r_arr = r_line.split("\t")
        self.idx = r_arr[0]
        self.result_str = r_arr[1]
        self.explain_str = r_arr[2]
    
    def get_idx_str(self):
        return str(self.idx)

    def get_result(self):
        return self.result_str

    def get_explain(self):
        return self.explain_str

class Home_t():

    def __init__(self, h_file_name):
        self.home_list = []
        # title \n explain
        for line in open(h_file_name, "r"):
            if "#" in line:
                continue
            for cont in line.split("\t"):
                self.home_list.append(cont)
    
    def get_title(self):
        return self.home_list[0]

    def get_explain(self):
        return self.home_list[1]
