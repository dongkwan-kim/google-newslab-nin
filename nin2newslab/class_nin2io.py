# IO helper class for NinX2

class ThumbnailGrid():
    def __init__(self, line):
        line_arr = line.split("/")
        self.label = line_arr[0]
        self.explain = line_arr[1]
        self.value = line_arr[2]
        self.ment = line_arr[3]

class RadioMatrix():
    def __init__(self, line):
        line_arr = line.split("/")
        self.label = line_arr[0]
        self.radio_list = line_arr[1:]

class SelectMatrix():
    def __init__(self, line):
        line_arr = line.split("/")
        self.label = line_arr[0]
        self.select_list = line_arr[1:]

class FormHorizontal():
    def __init__(self, string):
        str_arr = string.split("/")
        self.label = str_arr[0]
        self.inputtype = str_arr[1]
        self.name = str_arr[2]
        self.inputid = str_arr[3]
        self.placeholder = str_arr[4]
