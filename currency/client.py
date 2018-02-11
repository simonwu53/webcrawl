import tkinter
from tkinter import font
from currency import Bot
import time
import threading


class Client:
    def __init__(self, master):
        self.master = master
        master.title("Currency")

        # frames
        self.statistics_frame = tkinter.Frame(self.master)
        self.time_frame = tkinter.Frame(self.master)
        self.table_frame = tkinter.Frame(self.master)
        self.statistics_frame.grid(row=0, column=1)
        self.time_frame.grid(row=0, column=0)
        self.table_frame.grid(row=1, column=0, columnspan=2)

        # time_frame
        self.time_title = tkinter.Label(self.time_frame, text='Current Time: ')
        self.time_title.grid(row=0, column=0)
        self.time_var = tkinter.StringVar()
        self.time_label = tkinter.Label(self.time_frame, textvariable=self.time_var)
        self.time_label.grid(row=1, column=0)
        self.time_run()

        # statistics_frame
        self.min_var = tkinter.StringVar()
        self.min_var.set('Best Rate: ')
        self.min_label = tkinter.Label(self.statistics_frame, textvariable=self.min_var)
        self.min_label.grid(row=0, sticky=tkinter.W)

        self.trend_var = tkinter.StringVar()
        self.trend_var.set('Rate Trend: ')
        self.trend_label = tkinter.Label(self.statistics_frame, textvariable=self.trend_var)
        self.trend_label.grid(row=1, sticky=tkinter.W)

        self.se_var = tkinter.StringVar()
        self.se_var.set('Squared Error: ')
        self.se_label = tkinter.Label(self.statistics_frame, textvariable=self.se_var)
        self.se_label.grid(row=2, sticky=tkinter.W)

        # table_frame
        helv18 = font.Font(family="Helvetica", size=14, weight="bold")
        self.label_collection = []

        self.bank0 = tkinter.Label(self.table_frame, text='工商银行', font=helv18)
        self.bank0.grid(row=0, column=0)
        self.gs = tkinter.DoubleVar()
        self.gs_label = tkinter.Label(self.table_frame, textvariable=self.gs)
        self.gs_label.grid(row=1, column=0)
        self.gs_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.gs)

        self.bank1 = tkinter.Label(self.table_frame, text='中国银行', font=helv18)
        self.bank1.grid(row=0, column=1)
        self.zg = tkinter.DoubleVar()
        self.zg_label = tkinter.Label(self.table_frame, textvariable=self.zg)
        self.zg_label.grid(row=1, column=1)
        self.zg_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.zg)

        self.bank2 = tkinter.Label(self.table_frame, text='农业银行', font=helv18)
        self.bank2.grid(row=0, column=2)
        self.ny = tkinter.DoubleVar()
        self.ny_label = tkinter.Label(self.table_frame, textvariable=self.ny)
        self.ny_label.grid(row=1, column=2)
        self.ny_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.ny)

        self.bank3 = tkinter.Label(self.table_frame, text='交通银行', font=helv18)
        self.bank3.grid(row=0, column=3)
        self.jt = tkinter.DoubleVar()
        self.jt_label = tkinter.Label(self.table_frame, textvariable=self.jt)
        self.jt_label.grid(row=1, column=3)
        self.jt_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.jt)

        self.bank4 = tkinter.Label(self.table_frame, text='建设银行', font=helv18)
        self.bank4.grid(row=0, column=4)
        self.js = tkinter.DoubleVar()
        self.js_label = tkinter.Label(self.table_frame, textvariable=self.js)
        self.js_label.grid(row=1, column=4)
        self.js_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.js)

        self.bank5 = tkinter.Label(self.table_frame, text='招商银行', font=helv18)
        self.bank5.grid(row=2, column=0)
        self.zs = tkinter.DoubleVar()
        self.zs_label = tkinter.Label(self.table_frame, textvariable=self.zs)
        self.zs_label.grid(row=3, column=0)
        self.zs_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.zs)

        self.bank6 = tkinter.Label(self.table_frame, text='光大银行', font=helv18)
        self.bank6.grid(row=2, column=1)
        self.gd = tkinter.DoubleVar()
        self.gd_label = tkinter.Label(self.table_frame, textvariable=self.gd)
        self.gd_label.grid(row=3, column=1)
        self.gd_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.gd)

        self.bank7 = tkinter.Label(self.table_frame, text='浦发银行', font=helv18)
        self.bank7.grid(row=2, column=2)
        self.pf = tkinter.DoubleVar()
        self.pf_label = tkinter.Label(self.table_frame, textvariable=self.pf)
        self.pf_label.grid(row=3, column=2)
        self.pf_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.pf)

        self.bank8 = tkinter.Label(self.table_frame, text='兴业银行', font=helv18)
        self.bank8.grid(row=2, column=3)
        self.xy = tkinter.DoubleVar()
        self.xy_label = tkinter.Label(self.table_frame, textvariable=self.xy)
        self.xy_label.grid(row=3, column=3)
        self.xy_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.xy)

        self.bank9 = tkinter.Label(self.table_frame, text='中兴银行', font=helv18)
        self.bank9.grid(row=2, column=4)
        self.zx = tkinter.DoubleVar()
        self.zx_label = tkinter.Label(self.table_frame, textvariable=self.zx)
        self.zx_label.grid(row=3, column=4)
        self.zx_label.bind("<Button-1>", self.show_charts)
        self.label_collection.append(self.zx)

        self.refresh = tkinter.Button(self.table_frame, text='Refresh', command=self.refresh_currency)
        self.refresh.grid(row=4, column=0, columnspan=5, sticky=tkinter.NSEW)
        self.quit = tkinter.Button(self.table_frame, text='Quit', command=self.quit_client)
        self.quit.grid(row=5, column=0, columnspan=5, sticky=tkinter.NSEW)

        # init
        self.pricelist = None
        self.bot = Bot.Bot()
        self.refresh_currency()

    def refresh_currency(self):
        self.pricelist = None
        # get price list
        while True:
            self.pricelist = self.bot.get_pricelist()
            if self.pricelist:
                break
        bank, mini, trend, se_var = self.bot.get_statistics()

        # update ui
        for index, item in enumerate(self.pricelist):
            self.label_collection[index].set(self.pricelist[item][-1])
        self.min_var.set('Best Rate: %s (%s)' % (mini, bank))
        self.trend_var.set('Rate Trend: %s' % trend)
        self.se_var.set('Squared Error: %s' % se_var)

        # refresh
        self.refresh.after(900000, self.refresh_currency)

    def show_charts(self, e=None):
        chartview = Charts(self.master, self.pricelist)
        return

    def quit_client(self):
        self.bot.quit()
        self.master.quit()
        pass

    def time_run(self):
        localtime = time.asctime(time.localtime(time.time()))
        self.time_var.set(localtime)
        self.master.after(1000, self.time_run)


class Charts:
    def __init__(self, parent, pricelist):
        self.pricelist = pricelist
        self.top = tkinter.Toplevel(parent)
        self.top.title("Charts")
        # canvas
        self.c = tkinter.Canvas(self.top, width=300, height=100, bg='white')
        self.c.grid(row=0, column=0, columnspan=3)
        # select menu
        banklist = ['工商银行', '中国银行', '农业银行', '交通银行', '建设银行', '招商银行', '光大银行', '浦发银行', '兴业银行', '中兴银行']
        self.selected = tkinter.StringVar()
        self.bank_menu = tkinter.OptionMenu(self.top, self.selected, *banklist)
        self.bank_menu.grid(row=1, column=0, sticky=tkinter.NSEW)
        # button
        self.submit = tkinter.Button(self.top, text='Check', command=self.draw_canvas)
        self.submit.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.back = tkinter.Button(self.top, text='Back', command=self.destory_window)
        self.back.grid(row=1, column=2, sticky=tkinter.NSEW)

    def destory_window(self):
        self.top.destroy()

    def draw_canvas(self):
        self.c.delete('all')
        bank = self.selected.get()
        data = self.pricelist[bank]
        interval = int(300 / (len(data) + 1))
        pos_x = interval
        for point in data:
            pos_y = int(100 - float(point) / 10)
            self.c.create_rectangle(pos_x, pos_y, pos_x+10, 100, fill="blue")
            self.c.create_text(pos_x, pos_y, font=('Helvetica', 8), anchor=tkinter.SW, text=str(point))
            pos_x += interval


if __name__ == '__main__':
    root = tkinter.Tk()
    my_gui = Client(root)
    root.mainloop()
