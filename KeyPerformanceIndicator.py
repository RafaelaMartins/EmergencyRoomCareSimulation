import csv

class KeyPerformanceIndicator:

    def __init__(self):
        self.result = [['EXE','OCM','OCE','OCS','TER','TET','TEA','TEE','TAR','TAT','TAA','TAE']]    
        

    def calculate(self, e, i):
        self.result.append([i,
                            '{:.4f}'.format(self.idleness_time(e,e.doctors)),
                            '{:.4f}'.format(self.idleness_time(e,e.nurses)),
                            '{:.4f}'.format(self.idleness_time(e,e.secretaries)),
                            '{:.4f}'.format(self.mean_time_queue(e.registration_queue)),
                            '{:.4f}'.format(self.mean_time_queue(e.screening_queue)),
                            '{:.4f}'.format(self.mean_time_queue(e.medical_care_queue)),
                            '{:.4f}'.format(self.mean_time_queue(e.exam_medicine_queue)),
                            '{:.4f}'.format(self.mean_size_queue(e.registration_queue)),
                            '{:.4f}'.format(self.mean_size_queue(e.screening_queue)),
                            '{:.4f}'.format(self.mean_size_queue(e.medical_care_queue)),
                            '{:.4f}'.format(self.mean_size_queue(e.exam_medicine_queue))])

        self.write()
        self.result = []

    def idleness_time(self, e, entitys):
        entitys_amount = len(entitys)
        total_time = (e.simulation_time*entitys_amount)
        working_time = 0
        for e in entitys:
            working_time += e.working_time

        return (total_time-working_time)/total_time


    def mean_time_queue(self, queue):
        if queue.empty:
            return 0
        return sum(queue.time)/len(queue.time)

    def mean_size_queue(self, queue):
        if queue.empty:
            return 0
        return sum(queue.size)/len(queue.size)


    def write(self):
        with open('docs/kpi','a') as f:
            writer = csv.writer(f)
            writer.writerows(self.result)

#      self.result = 'EXE: Número da Execução\n'+\
#                      'OCM: Ociosidade Média Médicos(as)\n'+\
#                      'OCE: Ociosidade Média Enfermeiros(as)\n'+\
#                      'OCS: Ociosidade Média Secretários(as)\n'+\
#                      'TER: Tempo Médio fila de Registro\n'+\
#                      'TET: Tempo Médio fila de Triagem\n'+\
#                      'TEA: Tempo Médio Fila de Atendimento\n'+\
#                      'TEE: Tempo Médio Fila de Exames e Medicamentos\n'+\
#                      'TAR: Tamanho Médio fila de Registro\n'+\
#                      'TAT: Tamanho Médio fila de Triagem\n'+\
#                      'TAA: Tamanho Médio Fila de Atendimento\n'+\
#                      'TAE: Tamanho Médio Fila de Exames e Medicamentos\n\n'+\   
# ,'TAR','TAT','TAA','TAE']