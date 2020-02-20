# Local application imports
from Doctor import Doctor
from Secretary import Secretary
from Nurse import Nurse
from Patient import Patient
from calc import get_dist_num, get_exam_medicine, get_priority
from data import read_config
from Queue import Queue
from Log import Log
from KeyPerformanceIndicator import KeyPerformanceIndicator

class Emergency:

    def __init__(self, configuration_file):

        # global
        self.count = 0 # to control priority queue
        self.current_time = 0
        self.simulation_time = 0
        
        # employee sets
        self.nurses = set()
        self.doctors = set()
        self.secretaries = set()

        # priority queues
        self.event_queue = Queue(priority=True)
        self.medical_care_queue = Queue(priority=True)
        
        # other queues
        self.registration_queue = Queue()
        self.screening_queue = Queue()
        self.exam_medicine_queue = Queue()

        # config
        self.config = {}

        # Log
        self.log = Log()

        self.build(configuration_file)
        self.start()

# =================================================================
# BUILD
# =================================================================

    def build(self, configuration_file):
        
        self.config = read_config(configuration_file)
        
        self.simulation_time = float(self.config['T']['TTS'][0])
        self.create_employees()
        self.initialize_event_queue()
        self.log.header(self)

    def create_employees(self):
        config = self.config['Q']
        id = 1
        amount = int(config['MED'][0])
        for _ in range(amount):
            self.doctors.add(Doctor(id))
            id += 1
        amount = int(config['ENF'][0])
        for _ in range(amount):
            self.nurses.add(Nurse(id))
            id += 1
        amount = int(config['ATD'][0])
        for _ in range(amount):
            self.secretaries.add(Secretary(id))
            id += 1

    def initialize_event_queue(self):
        
        local_time = 0
        id = 0
        while local_time < self.simulation_time:
            duration = get_dist_num(self.config['T']['CHE'])
            exam_medicine = get_exam_medicine(self.config['P']['PRO'])
            priority = get_priority(self.config['P']['PRI'])
            id += 1
            local_time += duration
            patient = Patient(id, priority, exam_medicine)

            self.add_event(self.EndOfArrival(duration, local_time, patient))

# =================================================================
# EXECUTION
# =================================================================

    def start(self):
        event = self.next_event()
        while event.time < self.simulation_time:
            event.run(self)
            event = self.next_event()
        self.add_event(event)

        self.free_resources()
        self.log.write()
        
    def add_event(self, event):
        self.event_queue.insert(event, self.count)
        self.increment_count()

    def next_event(self):
        return self.event_queue.next()

    def add_queue(self, queue, entity):
        if not entity.priority:
            queue.insert(entity)
            queue.save_size()
        else:
            queue.insert(entity, self.count)
            self.count += 1
        entity.joined_queue = self.current_time
        queue.save_size()
        
    def rmv_queue(self, queue):
        patient = queue.next()
        queue.time.append(self.current_time - patient.joined_queue)
        patient.joined_queue = 0
        queue.save_size()
        return patient
                

    def free_resources(self):
        while not self.event_queue.empty:
            finalize = False    
            event = self.event_queue.next()

            if event.time-event.duration > self.simulation_time:
                finalize = True

            if event.__class__ == Emergency.EndOfRegistration:
                if not finalize:
                    event.secretary.working_time += \
                        (self.simulation_time - self.current_time)
                self.secretaries.add(event.secretary)
            elif event.__class__ in (Emergency.EndOfScreening, 
                                     Emergency.EndOfExamMedicine):
                if not finalize:
                    event.nurse.working_time += \
                        (self.simulation_time - self.current_time)
                self.nurses.add(event.nurse)
            elif event.__class__ == Emergency.EndOfMedicalCare:
                if not finalize:
                    event.doctor.working_time += \
                        (self.simulation_time - self.current_time)
                self.doctors.add(event.doctor)

    def increment_count(self):
        self.count += 1
            
# =================================================================
# EVENTS
# =================================================================

    class EndOfArrival():

        def __init__(self,  duration, time, patient):
            
            self.duration = duration
            self.time = time
            self.patient = patient

        def run(self, e):
            e.log.insert(("EndOfArrival",self))
            
            e.current_time = self.time
            
            if len(e.secretaries) > 0:
                secretary = e.secretaries.pop()
                duration = get_dist_num(e.config['T']['CAD'])
                execution_time = e.current_time + duration
                e.add_event(Emergency.EndOfRegistration(duration, execution_time, 
                                                    self.patient, secretary))
            else:
                e.add_queue(e.registration_queue, self.patient)

    class EndOfRegistration():

        def __init__(self,  duration, time, patient, secretary):

            self.duration = duration
            self.time = time
            self.patient = patient
            self.secretary = secretary

        def run(self, e):
            e.log.insert(("EndOfRegistration",self))
            
            e.current_time = self.time
            self.secretary.working_time += self.duration

            if not e.registration_queue.empty:
                duration = get_dist_num(e.config['T']['CAD'])
                patient = e.rmv_queue(e.registration_queue)
                execution_time = e.current_time + duration
                e.add_event(Emergency.EndOfRegistration(duration, execution_time, 
                                            patient, self.secretary))
            else:
                e.secretaries.add(self.secretary)

            if (self.patient.priority == 5):
                if len(e.doctors) > 0:
                    doctor = e.doctors.pop()
                    duration = get_dist_num(e.config['T']['ATE'])
                    execution_time = e.current_time + duration
                    e.add_event(Emergency.EndOfMedicalCare(duration, execution_time, 
                                                    self.patient, doctor))
                else: 
                    e.add_queue(e.medical_care_queue, self.patient)
            else:
                if len(e.nurses) > 0:
                    nurse = e.nurses.pop()
                    duration = get_dist_num(e.config['T']['TRI'])
                    execution_time = e.current_time + duration
                    e.add_event(Emergency.EndOfScreening(duration, execution_time,
                                                    self.patient, nurse))
                else:
                    e.add_queue(e.screening_queue, self.patient)

    class EndOfScreening():

        def __init__(self,  duration, time, patient, nurse):
            
            self.duration = duration
            self.time = time
            self.patient = patient
            self.nurse = nurse

        def run(self, e):
            e.log.insert(("EndOfScreening",self))

            e.current_time = self.time
            self.nurse.working_time += self.duration

            if not e.screening_queue.empty:
                duration = get_dist_num(e.config['T']['TRI'])
                execution_time = e.current_time + duration
                patient = e.rmv_queue(e.screening_queue)
                e.add_event(Emergency.EndOfScreening(duration, execution_time, patient,
                                        self.nurse))
            else:
                if not e.exam_medicine_queue.empty:
                    duration = get_dist_num(e.config['T']['EXA'])
                    execution_time = e.current_time + duration
                    patient = e.rmv_queue(e.exam_medicine_queue)
                    e.add_event(Emergency.EndOfExamMedicine(duration, execution_time,
                                                patient, self.nurse))
                else:
                    e.nurses.add(self.nurse)

            if len(e.doctors) > 0:
                doctor = e.doctors.pop()
                duration = get_dist_num(e.config['T']['ATE'])
                execution_time = e.current_time + duration
                e.add_event(Emergency.EndOfMedicalCare(duration, execution_time,
                                            self.patient, doctor))
            else:
                e.add_queue(e.medical_care_queue, self.patient)

    class EndOfExamMedicine():

        def __init__(self,  duration, time, patient, nurse):
            
            self.duration = duration
            self.time = time
            self.patient = patient
            self.nurse = nurse

        def run(self, e):
            e.log.insert(("EndOfExamMedicine",self))

            e.current_time = self.time
            self.nurse.working_time += self.duration

            if not e.exam_medicine_queue.empty:
                duration = get_dist_num(e.config['T']['EXA'])
                execution_time = e.current_time + duration
                patient = e.rmv_queue(e.exam_medicine_queue)
                e.add_event(Emergency.EndOfExamMedicine(duration, execution_time,
                                            patient, self.nurse))
            else:
                if not e.screening_queue.empty:
                    duration = get_dist_num(e.config['T']['TRI'])
                    execution_time = e.current_time + duration
                    patient = e.rmv_queue(e.screening_queue)
                    e.add_event(Emergency.EndOfScreening(duration, execution_time, patient,
                                            self.nurse))
                else:
                    e.nurses.add(self.nurse)

    class EndOfMedicalCare():

        def __init__(self,  duration, time, patient, doctor):
            
            self.duration = duration
            self.time = time
            self.patient = patient
            self.doctor = doctor

        def run(self, e):
            e.log.insert(("EndOfMedicalCare",self))
            
            e.current_time = self.time
            self.doctor.working_time += self.duration

            if not e.medical_care_queue.empty:
                patient = e.rmv_queue(e.medical_care_queue)
                duration = get_dist_num(e.config['T']['ATE'])
                execution_time = e.current_time + duration
                e.add_event(Emergency.EndOfMedicalCare(duration, execution_time, patient,
                                            self.doctor))
            else:
                e.doctors.add(self.doctor)

            if self.patient.exam_medicine:
                if len(e.nurses) > 0:
                    duration = get_dist_num(e.config['T']['EXA'])
                    execution_time = e.current_time + duration
                    nurse = e.nurses.pop()
                    e.add_event(Emergency.EndOfExamMedicine(duration, execution_time, 
                                                self.patient, nurse))
                else:
                    e.add_queue(e.exam_medicine_queue, self.patient)

if __name__ == '__main__':
    Emergency('docs/dados.txt')