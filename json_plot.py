import json
import sys
import numpy as np
import matplotlib.pyplot as plt

# TODO: this needs considerable optimisation and legibility improvements
# TODO: calculating mean/average triggered bugs if >1 runs

class Run():
    def __init__(self, fuzzer, target, program, run, reached, triggered):
        self.fuzzer = fuzzer
        self.target = target
        self.program = program
        self.run = run
        self.reached = reached
        self.triggered = triggered

    def __str__(self):
         return "{0} {1} {2} run #{3} | reached {4} triggered {5}".format(self.fuzzer, self.target, self.program, self.run, len(self.reached), len(self.triggered))

def generate_bugplot(json_path):
    """Triggered vs target"""
    
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
    
    
    ###################
    # Create the plot #
    ###################    
    fig, ax = plt.subplots()

    # we plot n_targets groups of n_fuzzer bars
    width = 0.85 / n_fuzzers
    print("WIDTH", width)
    x = np.arange(n_targets)
    k = np.arange(n_fuzzers)
    m = np.ceil( (k+1) /2)
    n = m * np.power(-1,k)

    print("n:",n)
    print("x:",x)

    if n_fuzzers %2 != 0:  # odd number of bars in groups needs shifting
        n = n - 0.5
    
    # DOBBO so what do I need to be able to plot?
    # so one line of code per fuzzer, but I need to have all targets ready
    # ahhh, now I can iterate through all the fuzzers in the JSON again, set all the bars heights to 0 by default
    # but update if the actual triggered value is found when iterating through all the fuzzers again
    for i_fuzzer,fuzzer in enumerate(data['results']):
        print("")
        print("I, FUZZER",i_fuzzer, fuzzer)
        bar_heights = np.zeros(n_targets)
        for i_target, target in enumerate(targets_list):
            print("")
            print("i, target",i_target, target)
            try:
                for program in data['results'][fuzzer][target]:
                    for run in data['results'][fuzzer][target][program]:
                        print("triggered:", data['results'][fuzzer][target][program][run]['triggered'])
                        bar_heights[i_target] += len(data['results'][fuzzer][target][program][run]['triggered'])
                        print("ttt:",target,bar_heights[i_target])
            except:
                print("Continued past", target)
                continue
        # whenever I plot, my position is x-n*(width) or x-n*(width/2)
        # here we need to do the ax.bar, as it needs to be done PER FUZZER as we need to set the positioning
        # so here we work out whether we are at width or width/2 depending on odd/even respectively
        print("ax.bar time!")
        print("DEBUG", n[i_fuzzer])
        ax.bar(x + n[i_fuzzer]*(width/2), bar_heights, width, label=fuzzer)

    ax.set_xticks(range(len(targets_list)), targets_list)
    ax.set_title("Mean number of bugs found for each target library")
    ax.set_xlabel("Targets")
    ax.set_ylabel("Number of bugs triggered")
    leg = ax.legend(loc="upper left", bbox_to_anchor=(1.04, 1.0))
    
    plt.savefig('bugplot.png', bbox_inches="tight")


def generate_sigplot(runs):
    raise NotImplementedError("Sigplot not yet implemented, sorry!")
    pass




def main():
    path = sys.argv[1]
    generate_bugplot(path)

if __name__ == "__main__":
    main()