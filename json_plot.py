import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# TODO: this needs considerable optimisation and legibility improvements
# TODO: calculating mean/average triggered bugs if >1 runs

def generate_bugplot(json_path, fig_path):
    """Read JSON summary file, save plot to fig_path"""
    
    with open(json_path, 'r') as json_file:
        data_str = json_file.read()

    data = json.loads(data_str)

    targets_list = []
    fuzzers_list = []

    for fuzzer in data['results']:
        if fuzzer not in fuzzers_list:
            fuzzers_list.append(fuzzer)
            print("Found fuzzer",fuzzer)
        for target in data['results'][fuzzer]:
            if target not in targets_list:
                targets_list.append(target)
                print("Target found:", target, "with fuzzer", fuzzer)
        
            
            for program in data['results'][fuzzer][target]:
                for run in data['results'][fuzzer][target][program]:
                    reached = data['results'][fuzzer][target][program][run]['reached']
                    triggered = data['results'][fuzzer][target][program][run]['triggered']
    
    n_targets = len(targets_list)
    n_fuzzers = len(fuzzers_list)
    print("Found", n_targets, "targets")
    print("Found", n_fuzzers, "fuzzers")

    # Now we create a dataframe, to make life easier when plotting later on
    df = pd.DataFrame(data=np.zeros(shape=(n_targets,n_fuzzers), dtype=int), index=targets_list, columns=fuzzers_list)

    # Loop through the JSON again to fill in the DF
    for fuzzer in data['results']:
        for target in data['results'][fuzzer]:
            for program in data['results'][fuzzer][target]:
                for run in data['results'][fuzzer][target][program]:
                    reached = data['results'][fuzzer][target][program][run]['reached']
                    triggered = data['results'][fuzzer][target][program][run]['triggered']
                    df.loc[target,fuzzer] += len(triggered)
    print("Total results found from", json_path,":")
    print(df)
    df = df.replace(to_replace=0, value=0.01)

    ###################
    # Create the plot #
    ###################    

    # A lot of this is based on https://stackoverflow.com/questions/59066811/how-can-a-plot-a-5-grouped-bars-bar-chart-in-matplotlib
    # One day, I'll get round to tweaking this to fix a few remaining undesirable behaviours
    # Notably the tick labelling being off-centre relative to the bars
    # TODO: update the tick labelling to more robust method given any number of bars in each group (i.e. any number of fuzzers)
    # TODO: label each bar with it's numerical value, to make easier than reading off y-axis?
    fig, ax = plt.subplots(figsize=(16,10))

    # Setting the positions and width for the bars
    pos = list(range(len(df)))
    num_col = len(df.columns)
    width = 0.95 / num_col

    bar_labels = df.index

    for i, (colname) in enumerate(df.columns):
        # 2 = 0.25
        # 3 = 0.2
        # 6 = 0.125
        delta_p = 0.2 + width*i
        plt.bar([p + delta_p for p in pos],
            df[colname], width, label=colname)

    ax.set_xticks(pos)
    def update_ticks(x, pos):
        return df.index[pos]

    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(ticker.FuncFormatter(update_ticks))
    ax.xaxis.set_minor_locator(ticker.FixedLocator([p+0.5 for p in pos]))
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('left')
    ylim = ax.get_ylim()
    ax.set_ylim(-0.05, ylim[-1])

    # plt.legend()
    # plt.grid()
    # plt.show()
    ax.set_title("Mean number of bugs found for each target library")
    ax.set_xlabel("Targets")
    ax.set_ylabel("Number of bugs triggered")
    leg = ax.legend(loc="upper left", bbox_to_anchor=(1.04, 1.0))
    plt.savefig(fig_path, bbox_inches="tight")
    print("Plot saved to", fig_path)


def main():
    json_path = sys.argv[1]
    fig_path = sys.argv[2]
    generate_bugplot(json_path, fig_path)

if __name__ == "__main__":
    main()