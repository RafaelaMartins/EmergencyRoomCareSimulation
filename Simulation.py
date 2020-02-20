from KeyPerformanceIndicator import KeyPerformanceIndicator
from Emergency import Emergency

class Simulation:

    def __init__(self):
        self.kpi = KeyPerformanceIndicator()
        self.run()

    def run(self):
        for i in range(100):
            e = Emergency('docs/dados.txt')
            self.kpi.calculate(e, i)

if __name__ == '__main__':
    Simulation()
