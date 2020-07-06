from pathlib import Path

class Observer():
    """Observer class to extract and save metrics of the system, environment and agents
    """
    def __init__(self):
        self.__general_filename = "data/data.csv"
        self.__init_file()

    def collect_metrics(self, time, agent, analyzer):
        g = agent.get_graph()
        adj = str(list(g.get_adjacency()))
        
        frequencies = str([d.get_frequency() for d in agent.get_data()])
        print(frequencies)

        metrics = "{};{};{};{};{};{}\n".format(time, str(type(agent)).split(".")[-1].replace("'>", ""), adj, frequencies, agent.get_frequencies(), analyzer.get_overlapping())
        if metrics != "":
            self.__write_in_file(metrics)

    ### Private functions
    def __init_file(self):
        Path(self.__general_filename).touch()

    def __write_in_file(self, metrics):
        f = open(self.__general_filename, "a+")
        f.write(metrics)
        f.close()