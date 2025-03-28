#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math



## adding extra columns
def add_extra_columns(df):
    # picking the filename and the subcategory from the filepath
    df["run_filename"] = df["run_name"].apply(lambda path : path.split("/")[-1])
    df["run_filename_clean"] = df["run_filename"].apply(lambda path : path.split(".")[0])
    df["run_subcategory"] = df["run_name"].apply(lambda path : path.split("/")[-2])
    return df

## tudying up the data
def tudy_up(df):
    # removing "s" from time values and turning them into float
    df["walltime"] = df["walltime"].apply(lambda time : float(time.replace("s", "")))
    df["cputime"] = df["cputime"].apply(lambda time : float(time.replace("s", "")))
    # removing "B" from memory values and turning them into int
    df["memory"] = df["memory"].apply(lambda mem : int(mem.replace("B", "")))
    return df




## main()

filepath = sys.argv[1]
df = pd.read_csv(filepath)
df = add_extra_columns(df)
df = tudy_up(df)

print(df.columns)

# just to check whether termination reason "cputime" means a TIMEOUT
# and "memory" means OUT OF MEMORY
#print(df[(df["terminationreason"] == "cputime")]["status"].unique()) 
#print(df[(df["terminationreason"] == "memory")]["status"].unique()) 
#print(df[(df["category"] == "error")]["status"].unique())
#print((df["category"] == "correct").unique())
#print((df["category"] == "wrong").unique())

df_correct = df[(df["category"] == "correct")]
df_correct_true = df_correct[(df_correct["run_expectedVerdict"] == True)]
df_correct_false = df_correct[(df_correct["run_expectedVerdict"] == False)]
df_wrong = df[(df["category"] == "wrong")]
df_wrong_true = df_wrong[(df_wrong["run_expectedVerdict"] == True)]
df_wrong_false = df_wrong[(df_wrong["run_expectedVerdict"] == False)]
df_timeout = df[(df["terminationreason"] == "cputime")]
df_oom = df[(df["terminationreason"] == "memory")]


## Generating a Figure "verdicts per benchmark"
df_verdict = pd.concat([df_correct, df_wrong], axis = 0)
#df_verdict_timeout_oom = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)

print(df["run_subcategory"].unique())
print(df_verdict)

for subcategory in df["run_subcategory"].unique():
    df_subcat = df_verdict[(df_verdict["run_subcategory"] == subcategory)].sort_values("run_filename_clean")
    labels = []
    times = []
    i = 0
    for task in df_subcat["run_filename_clean"].unique():
        df_task = df_subcat[(df_subcat["run_filename_clean"] == task)]
        times.append(df_task["cputime"])
        labels.append(task)
        for index, rec in df_task.iterrows():
            if (rec["category"] == "correct") & (rec["run_expectedVerdict"]):
                color = "green"
                marker = "^"
            if (rec["category"] == "correct") & (~rec["run_expectedVerdict"]):
                color = "green"
                marker = "v"
            if (rec["category"] == "wrong") & (rec["run_expectedVerdict"]):
                color = "red"
                marker = "^"
            if (rec["category"] == "wrong") & (~rec["run_expectedVerdict"]):
                color = "red"
                marker = "v"
            #if (rec["terminationreason"] == "cputime"):
            #    color = "black"
            #    marker = "x"
            #if (rec["terminationreason"] == "memory"):
            #    color = "black"
            #    marker = "+"
            plt.scatter(i, math.log(rec["cputime"] + 1), color=color, marker=marker)
        i = i + 1

    legend = [
            Line2D([0], [0], marker='^', color="white", markerfacecolor='green', label='correct true', markersize=9),
            Line2D([0], [0], marker='v', color="white", markerfacecolor='green', label='correct false', markersize=9),
            Line2D([0], [0], marker='^', color="white", markerfacecolor='red', label='incorrect true', markersize=9),
            Line2D([0], [0], marker='v', color="white", markerfacecolor='red', label='incorrect false', markersize=9),
            #Line2D([0], [0], marker='x', color="white", markeredgecolor='black', label='timeout', markersize=7),
            #Line2D([0], [0], marker='+', color="white", markeredgecolor='black', label='out of memory', markersize=9),
            ]

    plt.title(str("Subcategory: " + subcategory))
    plt.xlabel("Benchmark name")
    plt.ylabel("CPU time [log(time + 1)]")
    plt.xticks(range(0, len(labels)), labels = labels, rotation=90)
    plt.tight_layout()
    #plt.ylim(-30, 1000)
    plt.ylim(-1, 10)
    plt.xlim(-1, len(labels))
    plt.legend(handles=legend)
    plt.show()


# only final verdicts and timeouts
#df_verdict_and_timeout
