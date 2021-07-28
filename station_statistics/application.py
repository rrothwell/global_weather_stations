

class Application():

    def __init__(self, loader, collector, reporter):
        self.loader = loader
        self.collector = collector
        self.reporter = reporter
        return


    def initialise(self):
        return


    def run(self):
        metadatas = self.loader.load()
        statistics = self.collector.collect_statistics(metadatas)
        self.reporter.report(statistics)
        return
