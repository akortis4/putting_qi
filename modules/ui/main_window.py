import tkinter as tk
from tkinter.ttk import Frame, Label, Entry, Button

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x = int(self.winfo_screenwidth() / 2 - 640)
        y = int(self.winfo_screenheight() / 2 - 360)

        self.geometry(f'1280x720+{x}+{y}')
        self.title('QI Putting App')

        self.top_labels = ['Distance from Basket'
                            , 'Made'
                            , 'Missed High'
                            , 'Missed High/Right'
                            , 'Missed Right'
                            , 'Missed Low/Right'
                            , 'Missed Low'
                            , 'Missed Low/Left'
                            , 'Missed Left'
                            , 'Missed High/Left'
                            , 'Chain Out'
                            , 'Foot Fault']
        
        # date frame variables
        self.date_frame = Frame(self)
        self.entry_date = tk.StringVar()
        

        # top label frame variables
        self.top_label_frames = []
        self.top_labels = ['Distance from Basket'
                            , 'Made'
                            , 'Missed High'
                            , 'Missed High/Right'
                            , 'Missed Right'
                            , 'Missed Low/Right'
                            , 'Missed Low'
                            , 'Missed Low/Left'
                            , 'Missed Left'
                            , 'Missed High/Left'
                            , 'Chain Out'
                            , 'Foot Fault'
                            , 'Total'
                            , 'Percent Made']
        
        # distance labels
        self.distance_label_frames = []
        self.distance_labels = ['2 Meters'
                                , '4 Meters'
                                , '6 Meters'
                                , '8 Meters'
                                , '10 Meters'
                                , 'Total']
        
        # putt frames
        self.putt_frames = []
        self.putt_variables = []

        # row total/percent frames
        self.row_total_frames = []
        self.row_percent_frames = []
        self.row_total_variables = []
        self.row_percent_variables = []
        
        # column total/percent frames
        self.col_total_frames = []
        self.col_total_variables = []

        # aggregate total frames
        self.aggregate_total_frame = Frame(self)
        self.aggregate_total_variable = tk.IntVar(self.aggregate_total_frame, value=0)
        self.aggregate_percent_variable = tk.StringVar(self.aggregate_total_frame, value='0%')

        # create submit frame
        self.submit_frame = Frame(self)
        
        self.execute()

    def execute(self):
        self.create_date_label()
        self.create_top_labels()
        self.create_distance_labels()   
        self.create_putt_frames()   
        self.create_row_total_frames()
        self.create_col_total_frames()
        self.create_aggregate_frames()
        self.create_submit_frame()

    def create_date_label(self):
        Label(self.date_frame, text='Date:').pack()
        Label(self.date_frame, text='(MM/DD/YYYY)').pack()
        Entry(self.date_frame, textvariable=self.entry_date).pack()
        self.date_frame.grid(row=0, column=0, columnspan=14)

    def create_top_labels(self):
        for x, name in enumerate(self.top_labels):
            frame = Frame(self)
            Label(frame, text=name).pack()
            self.top_label_frames.append(frame)
            frame.grid(row=1, column=x)

    def create_distance_labels(self):
        for x, name in enumerate(self.distance_labels):
            frame = Frame(self)
            Label(frame, text=name).pack()
            self.distance_label_frames.append(frame)
            frame.grid(row=x+2, column=0)

    def create_putt_frames(self):
        for x in range(5):
            temp_frames = []
            temp_variables = []
            for y in range(11):
                frame = Frame(self)
                var_count = tk.IntVar(frame, value=0)
                Label(frame, text=str(var_count.get()), textvariable=var_count).grid(row=0, column=0, columnspan=2)
                Button(frame, text='+', width=5, command=lambda row=x, column=y: self.increase(row, column)).grid(row=1, column=0)
                Button(frame, text='-', width=5, command=lambda row=x, column=y: self.decrease(row, column)).grid(row=1, column=1)
                frame.grid(row=x+2, column=y+1)
                temp_frames.append(frame)
                temp_variables.append(var_count)
            self.putt_frames.append(temp_frames)
            self.putt_variables.append(temp_variables)

    def create_row_total_frames(self):
        for x in range(5):
            total_frame = Frame(self)
            percent_frame = Frame(self)
            var_total = tk.IntVar(total_frame, value=0)
            var_percent = tk.StringVar(percent_frame, value='0%')
            Label(total_frame, text=var_total.get(), textvariable=var_total).pack()     
            Label(percent_frame, textvariable=var_percent).pack()
            total_frame.grid(row=x+2, column=13)  
            percent_frame.grid(row=x+2, column=14)
            self.row_total_frames.append(total_frame)
            self.row_percent_frames.append(percent_frame)
            self.row_total_variables.append(var_total)
            self.row_percent_variables.append(var_percent)         

    def create_col_total_frames(self):
        for y in range(11):
            total_frame = Frame(self)
            var_total = tk.IntVar(total_frame, value=0)
            Label(total_frame, text=var_total.get(), textvariable=var_total).pack()
            total_frame.grid(row=7, column=y+1)
            self.col_total_frames.append(total_frame)
            self.col_total_variables.append(var_total)
            
    def create_aggregate_frames(self):
        Label(self.aggregate_total_frame, textvariable=self.aggregate_total_variable).grid(row=0, column=0)
        Label(self.aggregate_total_frame, textvariable=self.aggregate_percent_variable).grid(row=0, column=1)
        self.aggregate_total_frame.grid(row=7, column=12, columnspan=2, rowspan=2)

    def create_submit_frame(self):
        Button(self.submit_frame, text='Submit Data').pack()
        self.submit_frame.grid(row=9, column=0, columnspan=13)

    def increase(self, row, column):
        self.putt_variables[row][column].set(self.putt_variables[row][column].get() + 1)
        self.increase_row_total(row)
        self.increase_col_total(column)
        self.increase_aggregate_total()
        self.update_row_percent(row)
        self.update_aggregate_percent()
        self.update()

    def decrease(self, row, column):
        if self.putt_variables[row][column].get() <= 0:
            self.putt_variables[row][column].set(0)
        else:
            self.putt_variables[row][column].set(self.putt_variables[row][column].get() - 1)
            self.decrease_row_total(row)
            self.decrease_col_total(column)
            self.decrease_aggregate_total()
            self.update_row_percent(row)
            self.update_aggregate_percent()
        self.update()

    def increase_row_total(self, row):
        self.row_total_variables[row].set(self.row_total_variables[row].get() + 1)

    def decrease_row_total(self, row):
        if self.row_total_variables[row].get() <= 0:
            self.row_total_variables[row].set(0)
        else:
            self.row_total_variables[row].set(self.row_total_variables[row].get() - 1)

    def increase_col_total(self, col):
        self.col_total_variables[col].set(self.col_total_variables[col].get() + 1)

    def decrease_col_total(self, col):
        if self.col_total_variables[col].get() <= 0:
            self.col_total_variables[col].set(0)
        else:
            self.col_total_variables[col].set(self.col_total_variables[col].get() - 1)

    def increase_aggregate_total(self):
        self.aggregate_total_variable.set(self.aggregate_total_variable.get() + 1)

    def decrease_aggregate_total(self):
        if self.aggregate_total_variable.get() <= 0:
            self.aggregate_total_variable.set(0)
        else:
            self.aggregate_total_variable.set(self.aggregate_total_variable.get() - 1)

    def update_row_percent(self, row):
        percent = (self.putt_variables[row][0].get() / self.row_total_variables[row].get()) * 100
        self.row_percent_variables[row].set(f'{round(percent, 2)}%')

    def update_aggregate_percent(self):
        percent = (self.col_total_variables[0].get() / self.aggregate_total_variable.get()) * 100
        self.aggregate_percent_variable.set(f'{round(percent, 2)}%')