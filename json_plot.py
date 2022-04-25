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

def load_runs(json_path):
    """Loads in a magma summary json file, stores the data in a Run object"""
    
    loaded_runs = []
    
    with open(json_path, 'r') as json_file:
        data_str = json_file.read()

    data = json.loads(data_str)

    for fuzzer in data['results']:
        for target in data['results'][fuzzer]:
            for program in data['results'][fuzzer][target]:
                for run in data['results'][fuzzer][target][program]:
                    reached = data['results'][fuzzer][target][program][run]['reached']
                    triggered = data['results'][fuzzer][target][program][run]['triggered']
                    loaded_run = Run(fuzzer, target, program, run, reached, triggered)
                    # print(loaded_run)
                    loaded_runs.append(loaded_run)
    return loaded_runs

def generate_bugplot(runs):
    """Triggered vs target"""
    
    ##########################
    # Calculate what to plot #
    ##########################
    targets = {}
    fuzzers = {}
    
    # Group the runs by their targets and by their fuzzers
    # By storing a dictionary of {target/fuzzer:position in runs list}
    # This allows us to create the grouped bar chart later
    for i,run in enumerate(runs):
        target = run.target
        fuzzer = run.fuzzer
        
        if target not in targets:
            targets[target] = []
        targets[target].append(i)

        if fuzzer not in fuzzers:
            fuzzers[fuzzer] = []
        fuzzers[fuzzer].append(i)
    
    n_targets = len(targets)
    n_fuzzers = len(fuzzers)

    data_to_plot = {}
    for target in targets:
        this_target = {}    
        for i in targets[target]:  # loop through all the runs against this target, with any fuzzer
            fuzzer = runs[i].fuzzer
            if fuzzer not in this_target:
                this_target[fuzzer] = 0
            triggered = len(runs[i].triggered)
            this_target[fuzzer] = (this_target[fuzzer] + triggered)
        data_to_plot[target] = this_target

    width = 0.85 / len(fuzzers)
    
    ###################
    # Create the plot #
    ###################    
    fig, ax = plt.subplots()
              
    ax.set_xticks(range(1,len(targets)+1), targets.keys())
    ax.set_title("Mean number of bugs found for each target library")
    ax.set_xlabel("Targets")
    ax.set_ylabel("Number of bugs triggered")
    leg = ax.legend(loc="upper left", bbox_to_anchor=(1.04, 1.0))
    
    plt.savefig('bugplot.png', bbox_inches="tight")


def generate_sigplot(runs):
    raise NotImplementedError("Sigplot not yet implemented, sorry!")
    pass




def main():
    if not "bugplot" in sys.argv and not "sigplot" in sys.argv:
        print("No plots specified, exiting...")  # not passing str to sys.exit else "abnormal" output, so goes to stderr
        sys.exit(0)

    path = sys.argv[1]
    runs = load_runs(path)
    # print("Total runs:", len(runs))

    if "bugplot" in sys.argv:
        generate_bugplot(runs)

    if "sigplot" in sys.argv:
        pass
        # generate_sigplot(runs)

    

if __name__ == "__main__":
    main()

