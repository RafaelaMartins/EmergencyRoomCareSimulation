from datetime import datetime
class Log:

    def __init__(self):

        self.log = ''

    def header(self, e):
        self.log = 'HORA: {}\n'.format(datetime.now()) + \
                   'Tempo de Simulação: {}\n'.format(e.simulation_time) + \
                   'Número de Secretários(as): {}\n'.format(len(e.secretaries)) + \
                   'Número de Enfermeiros(as): {}\n'.format(len(e.nurses)) + \
                   'Número de Médicos(as): {}\n'.format(len(e.doctors)) 

    def insert(self, log):
        name, event = log
        self.log += '\n\nEVENT={} : Time={}, Duration={}, '.format(name, event.time,
                                                       event.duration) + \
                    'Patient={} '.format(event.patient.id)
        if name == 'EndOfRegistration':
            self.log += 'Secretary={}'.format(event.secretary.id)
        elif name in ('EndOfScreening','EndOfExamMedicine'):
            self.log += 'Nurse={}'.format(event.nurse.id)
        elif name == 'EndOfMedicalCare':
            self.log += 'Doctor={}'.format(event.doctor.id)
        
    def write(self):
        with open("docs/log","w") as f:
            f.write(self.log)