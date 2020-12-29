from dearpygui.core import *
from dearpygui.simple import *
from screeninfo import get_monitors
import openpyxl as xl
import numpy as np
import pandas as pd
import csv, os, re, shutil


#### GLOBAL VARIABLES ####
headers = ''
screen = get_monitors()[0]
s_w = int(screen.width/2)
s_h = int(screen.height/2)
arr_test = []
df = pd.DataFrame()
# pd.set_option('display.max_rows', None)


#### FUNCTION DEFINITIONS ####


def select_file(sender, data):
    open_file_dialog(callback=update_file_label, extensions=".csv")


def update_file_label(sender, data):
    csv_path = data[0]+"/"+data[1]
    set_value("lbl_path", str(csv_path))
    print(csv_path)
    with open(str(csv_path)) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        dt = [row for row in reader]
    configure_item("source_data", items=dt[0])
    configure_item("column_destination", items=dt[0])
    headers = dt[0]
    add_value("dt", dt)
    set_value("dt", dt)
    df = pd.DataFrame(columns = headers)


def get_vals(sender, data):

    src = get_value("source_data")
    # print(len(src))
    if len(src) != 0:
        if src == "all":
            get_vals_all_data()
        else:
            get_vals_single_col(src)
    else:
        print("please select source_data")
    

def get_vals_single_col(src):
    show_logger()
    log_info("...")
    log_info("analyzing data......")
    rx = get_value(name="rxp")
    for e in range(0, len(dt)):
        row = dt[e]
        if re.match(rx,row[0]):
            log_info("match: " + "row-" + str(e+1) + "-" + str(row[0]))
            print(row[0])

def get_vals_all_data():
    csv_path = get_value("lbl_path")
    with open(str(csv_path)) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        dt = [row for row in reader]
    df = pd.DataFrame(columns = dt[0])
    got_match = 0
    len_header = len(dt[0])
    clear_log()
    show_logger()
    log_info("analyzing data...")
    rx = get_value(name="rxp")
    for r in range(len(dt)):
        row = dt[r]
        if len(row) < len_header:
            print("row " + str(r) + " length doesnt match header length")
            diff = len_header - len(row)
            for i in range(0, diff):
                row.append("")
        for c in range(len_header):
            cell = row[c]
            if re.match(rx,cell):
                got_match = 1
                arr_test.append(cell)
        if got_match == 0:
            print("no match on row " + str(r))
            arr_test.append("")
        got_match = 0
    dest = get_value("column_destination")
    df[dest] = arr_test
    arr_test.clear()
    log_info("logging dataframe...")
    log_info(df)




    
def save_csv_file(sender, data):
    df.to_csv('newdata.csv', index = True) 


def main():

    #### MAIN PROGRAM ####

    set_main_window_size(s_w, s_h)
    set_main_window_pos(int(s_w/2), int(s_h/2))
    set_main_window_title("SheetyApp")
    with window("main"):
        with tab_bar("tabs"):
            with tab("test"):

                # pick csv file #
                add_button("browse", callback=select_file)
                add_same_line(spacing=10)
                add_label_text("lbl_path")
                

                # inputs #
                add_input_text("rxp", width=240)
                add_combo("source_data", items=[""], default_value="all", width=240)
                add_combo("column_destination", items=[""], default_value="", width=240)
                

                # buttons #
                add_button("run", callback=get_vals)
                add_same_line(spacing=10)
                add_button("export", callback=save_csv_file)


            with tab("analyze"):
                add_table("table##widget", ["Column 1", "Column 2", "Column 3", "Column 4"])
                tabledata = []
                for i in range(0, 4):
                    row = []
                    for j in range(0, 4):
                        # print(dt[i][j])
                        row.append("")
                    tabledata.append(row)

                set_value("table##widget", tabledata)

    start_dearpygui(primary_window="main")

if __name__ == "__main__":
    main()
