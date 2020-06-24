class Observer:
    def __init__(self):
        self.__general_filename = "data/data.csv"
        self.__specific_filename = "data/{}_{}_{}.csv".format(self.__env.get_sheets_count(), len(self.__agents), datetime.now().strftime("%d%m%Y%H%M%S"))
        self.__init_file()

    def collect_metrics(self, agents):
        metrics = ""
        for (agent, stage) in agents:
            metrics = "{},{},{},{},{},{},{}\n".format(self.__env.get_distribution(), self.__time, self.__env.get_sheets_count(), agent.get_metrics(), len(self.__agents), len(self.__full_agents), stage)
        if metrics != "":
            self.__write_in_file(metrics)

    ### Private functions
    def __init_file(self):
        Path(self.__general_filename).touch()

    def __write_in_file(self, metrics):
        f = open(self.__general_filename, "a+")
        f.write(metrics)
        f.close()