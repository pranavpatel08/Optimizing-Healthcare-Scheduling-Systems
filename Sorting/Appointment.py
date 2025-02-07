import csv
from datetime import datetime


class Appointment:
    def __init__(self, patient_id: str, scheduled_date: datetime.date, scheduled_time: datetime.time, duration_minutes: int, required_resources: str, priority_score: int, condition_type: str, wait_time_target: int):
        self.patient_id = patient_id
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
        self.required_resources = required_resources
        self.priority_score = priority_score
        self.condition_type = condition_type
        self.wait_time_target = wait_time_target

    def __repr__(self):
        return (f"Appointment(patient_id={self.patient_id}, scheduled_date={self.scheduled_date}, "
                f"scheduled_time={self.scheduled_time}, duration_minutes={
                    self.duration_minutes}, "
                f"required_resources={self.required_resources}, priority_score={
                    self.priority_score}, "
                f"condition_type={self.condition_type}, wait_time_target={self.wait_time_target})")


class AppointmentList:
    def __init__(self, filename: str):
        self.appointments = []
        self.load_appointments(filename)

    def load_appointments(self, filename: str):
        with open(filename, mode='r') as file:
            data = csv.DictReader(file)
            for row in data:
                scheduled_datetime = datetime.strptime(
                    f"{row['scheduled_date']} {row['scheduled_time']}", "%Y-%m-%d %H:%M")
                appointment = Appointment(
                    patient_id=row['patient_id'],
                    scheduled_date=scheduled_datetime.date(),
                    scheduled_time=scheduled_datetime.time(),
                    duration_minutes=int(row['duration_minutes']),
                    required_resources=row['required_resources'],
                    priority_score=int(row['priority_score']),
                    condition_type=row['condition_type'],
                    wait_time_target=int(row['wait_time_target'])
                )
                self.appointments.append(appointment)

    def sort_all(self):
        condition_priority = {'Emergency': 0, 'Urgent': 1, 'Routine': 2}
        sorted_appointments = sorted(self.appointments, key=lambda x: (
            x.scheduled_date,
            x.scheduled_time,
            condition_priority[x.condition_type],
            x.priority_score
        ))
        return sorted_appointments
    
    def save_sorted_appointments(self, sorted_appointments, output_filename):
        with open(output_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['patient_id', 'scheduled_date', 'scheduled_time', 'duration_minutes',
                                'required_resources', 'priority_score', 'condition_type', 'wait_time_target'])

            # Write each appointment
            for appt in sorted_appointments:
                writer.writerow([
                    appt.patient_id,
                    appt.scheduled_date,
                    appt.scheduled_time,
                    appt.duration_minutes,
                    appt.required_resources,
                    appt.priority_score,
                    appt.condition_type,
                    appt.wait_time_target
                ])

    def __repr__(self):
        return f"AppointmentList(appointments={self.appointments})"
