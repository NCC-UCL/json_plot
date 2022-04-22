import json
import sys

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
                    print(loaded_run)
                    loaded_runs.append(loaded_run)
    return loaded_runs

def main():
    path = sys.argv[1]
    runs = load_runs(path)
    print("Total runs:", len(runs))
                    
if __name__ == "__main__":
    main()

