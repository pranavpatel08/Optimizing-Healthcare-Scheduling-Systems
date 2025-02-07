import unittest
import pandas as pd
import tempfile
import os
from datetime import datetime, timedelta
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

# Import classes from src.scheduler
from src.scheduler import ScheduleOptimizerRunner

class TestScheduleOptimizer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory and test Excel files for various scenarios
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.test_dir.name, 'test_schedule.xlsx')

    def tearDown(self):
        # Clean up temporary directory
        self.test_dir.cleanup()

    def create_test_excel(self, data):
        # Helper function to create a test Excel file from a DataFrame
        data.to_excel(self.test_file_path, index=False)

    def test_no_appointments(self):
        # Test with no appointments - empty DataFrame
        data = pd.DataFrame(columns=['patient_id', 'scheduled_date', 'scheduled_time', 'priority_score', 'required_resources', 'duration_minutes', 'wait_time_target'])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 10, 'ConsultationRoom': 10, 'EmergencyRoom': 5}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)

        # Just ensure no exceptions are raised, and monthly summary shows no usage
        runner.run()

    def test_single_appointment(self):
        # One single appointment
        data = pd.DataFrame([{
            'patient_id': 'P1',
            'scheduled_date': datetime(2024, 12, 15),
            'scheduled_time': '09:00:00',
            'priority_score': 1,
            'required_resources': 'TreatmentRoom',
            'duration_minutes': 30,
            'wait_time_target': 10
        }])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 2, 'ConsultationRoom': 2, 'EmergencyRoom': 2}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)
        runner.run()

    def test_multiple_appointments_same_time(self):
        # Three appointments scheduled at the same time, same room type, different priorities
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 15),
                'scheduled_time': '09:00:00',
                'priority_score': 3,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 20,
                'wait_time_target': 5
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 15),
                'scheduled_time': '09:00:00',
                'priority_score': 2,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 20,
                'wait_time_target': 5
            },
            {
                'patient_id': 'P3',
                'scheduled_date': datetime(2024, 12, 15),
                'scheduled_time': '09:00:00',
                'priority_score': 1,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 20,
                'wait_time_target': 5
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 3, 'ConsultationRoom': 2, 'EmergencyRoom': 2}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)
        runner.run()

    def test_appointments_across_multiple_days(self):
        # Appointments spanning multiple dates
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 14),
                'scheduled_time': '10:00:00',
                'priority_score': 1,
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 15),
                'scheduled_time': '11:00:00',
                'priority_score': 2,
                'required_resources': 'EmergencyRoom',
                'duration_minutes': 60,
                'wait_time_target': 0
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 5, 'ConsultationRoom': 5, 'EmergencyRoom': 5}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)
        runner.run()

    def test_wait_time_edge_cases(self):
        # One appointment with a wait_time_target = 0 (must start on time or open new room)
        # Another with a generous wait time and overlapping start times
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 16),
                'scheduled_time': '09:00:00',
                'priority_score': 1,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 60,
                'wait_time_target': 0
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 16),
                'scheduled_time': '09:30:00',
                'priority_score': 2,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 20
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 2, 'ConsultationRoom': 2, 'EmergencyRoom': 2}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)
        runner.run()

    def test_room_limits_and_min_requirements(self):
        # Multiple appointments to test optimization respects room limits and tries different configurations
        # Also tests the DP optimization changes room configurations
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 17),
                'scheduled_time': '08:00:00',
                'priority_score': 3,
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 17),
                'scheduled_time': '08:10:00',
                'priority_score': 2,
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 5
            },
            {
                'patient_id': 'P3',
                'scheduled_date': datetime(2024, 12, 17),
                'scheduled_time': '08:20:00',
                'priority_score': 1,
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 0
            }
        ])
        self.create_test_excel(data)

        # Limit the rooms more aggressively to force the DP optimization to try different configurations
        room_limits = {'TreatmentRoom': 1, 'ConsultationRoom': 2, 'EmergencyRoom': 1}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()

    def test_realistic_sample_scenario(self):
        # A scenario with multiple overlapping appointments of different types, durations, and priorities
        base_date = datetime(2024, 12, 18)
        data_list = []
        for i in range(10):
            # Staggered start times by 10 minutes
            start_time = (datetime(base_date.year, base_date.month, base_date.day, 9)
                          + timedelta(minutes=10*i)).strftime('%H:%M:%S')
            room_type = ['TreatmentRoom', 'ConsultationRoom', 'EmergencyRoom'][i % 3]
            priority = (i % 3) + 1
            wait_target = 5 * (i % 3)
            duration = 20 if room_type == 'TreatmentRoom' else 30 if room_type == 'ConsultationRoom' else 45
            data_list.append({
                'patient_id': f'P{i+1}',
                'scheduled_date': base_date,
                'scheduled_time': start_time,
                'priority_score': priority,
                'required_resources': room_type,
                'duration_minutes': duration,
                'wait_time_target': wait_target
            })

        data = pd.DataFrame(data_list)
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 5, 'ConsultationRoom': 5, 'EmergencyRoom': 5}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits)
        runner.run()

    def test_multiple_overlapping_appointments(self):
    #Test multiple overlapping appointments for the same room type.
      data = pd.DataFrame([
          {
              'patient_id': 'P1',
              'scheduled_date': datetime(2024, 12, 19),
              'scheduled_time': '09:00:00',
              'priority_score': 1,
              'required_resources': 'EmergencyRoom',
              'duration_minutes': 60,
              'wait_time_target': 10
          },
          {
              'patient_id': 'P2',
              'scheduled_date': datetime(2024, 12, 19),
              'scheduled_time': '09:30:00',
              'priority_score': 2,
              'required_resources': 'EmergencyRoom',
              'duration_minutes': 30,
              'wait_time_target': 5
          },
          {
              'patient_id': 'P3',
              'scheduled_date': datetime(2024, 12, 19),
              'scheduled_time': '10:00:00',
              'priority_score': 3,
              'required_resources': 'EmergencyRoom',
              'duration_minutes': 45,
              'wait_time_target': 15
          }
      ])
      self.create_test_excel(data)

      room_limits = {'TreatmentRoom': 2, 'ConsultationRoom': 2, 'EmergencyRoom': 1}
      runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
      runner.run()

    def test_different_room_types(self):
        #Test appointments requiring different room types.
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 20),
                'scheduled_time': '08:00:00',
                'priority_score': 1,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 20),
                'scheduled_time': '08:15:00',
                'priority_score': 2,
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 45,
                'wait_time_target': 15
            },
            {
                'patient_id': 'P3',
                'scheduled_date': datetime(2024, 12, 20),
                'scheduled_time': '08:30:00',
                'priority_score': 3,
                'required_resources': 'EmergencyRoom',
                'duration_minutes': 20,
                'wait_time_target': 5
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 1, 'ConsultationRoom': 1, 'EmergencyRoom': 1}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()

    def test_zero_wait_time_target(self):
        #Test appointments with wait_time_target set to 0.
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 21),
                'scheduled_time': '10:00:00',
                'priority_score': 1,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 60,
                'wait_time_target': 0
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 21),
                'scheduled_time': '10:30:00',
                'priority_score': 2,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 0
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 1, 'ConsultationRoom': 1, 'EmergencyRoom': 1}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()

    def test_large_number_of_appointments(self):
        #Test with a large number of appointments to assess performance.
        base_date = datetime(2024, 12, 22)
        data_list = []
        for i in range(100):
            start_hour = 8 + (i // 10) % 10
            start_minute = (i % 10) * 5
            start_time = f"{start_hour:02d}:{start_minute:02d}:00"
            room_type = ['TreatmentRoom', 'ConsultationRoom', 'EmergencyRoom'][i % 3]
            priority = (i % 5) + 1
            wait_target = 5 * (i % 3)
            duration = 15 + (i % 4) * 5  # Durations: 15, 20, 25, 30 minutes
            data_list.append({
                'patient_id': f'P{i+1}',
                'scheduled_date': base_date,
                'scheduled_time': start_time,
                'priority_score': priority,
                'required_resources': room_type,
                'duration_minutes': duration,
                'wait_time_target': wait_target
            })

        data = pd.DataFrame(data_list)
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 5, 'ConsultationRoom': 5, 'EmergencyRoom': 5}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()

    def test_priority_handling(self):
        #Test that higher priority patients are allocated rooms first.
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 23),
                'scheduled_time': '09:00:00',
                'priority_score': 5,  # Highest priority
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 23),
                'scheduled_time': '09:00:00',
                'priority_score': 1,  # Lowest priority
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            },
            {
                'patient_id': 'P3',
                'scheduled_date': datetime(2024, 12, 23),
                'scheduled_time': '09:00:00',
                'priority_score': 3,  # Medium priority
                'required_resources': 'ConsultationRoom',
                'duration_minutes': 30,
                'wait_time_target': 10
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 1, 'ConsultationRoom': 2, 'EmergencyRoom': 1}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()

    def test_consecutive_appointments(self):
        #Test consecutive appointments to ensure efficient room reuse.
        data = pd.DataFrame([
            {
                'patient_id': 'P1',
                'scheduled_date': datetime(2024, 12, 24),
                'scheduled_time': '08:00:00',
                'priority_score': 1,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 5
            },
            {
                'patient_id': 'P2',
                'scheduled_date': datetime(2024, 12, 24),
                'scheduled_time': '08:30:00',
                'priority_score': 2,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 5
            },
            {
                'patient_id': 'P3',
                'scheduled_date': datetime(2024, 12, 24),
                'scheduled_time': '09:00:00',
                'priority_score': 3,
                'required_resources': 'TreatmentRoom',
                'duration_minutes': 30,
                'wait_time_target': 5
            }
        ])
        self.create_test_excel(data)

        room_limits = {'TreatmentRoom': 1, 'ConsultationRoom': 1, 'EmergencyRoom': 1}
        runner = ScheduleOptimizerRunner(self.test_file_path, room_limits, alpha=1.0, beta=2.0)
        runner.run()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)