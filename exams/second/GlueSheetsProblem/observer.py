from pathlib import Path

class Observer:
    def __init__(self):
        self.__general_filename = "data/data.csv"
        self.__init_file()

    def collect_metrics(self, time, agents_completed, distribution, agents_count, full_agents):
        metrics = ""
        for (agent, stage) in agents_completed:
            metrics = "{},{},{},{},{},{},{}\n".format(distribution, time, agent.get_album_size(), agent.get_metrics(), agents_count, full_agents, stage)
        if metrics != "":
            self.__write_in_file(metrics)

    ### Private functions
    def __init_file(self):
        Path(self.__general_filename).touch()

    def __write_in_file(self, metrics):
        f = open(self.__general_filename, "a+")
        f.write(metrics)
        f.close()