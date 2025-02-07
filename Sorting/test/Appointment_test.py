import unittest
from Appointment import AppointmentList

class AppointmentListTest(unittest.TestCase):
    def setUp(self):
        self.appointment_list = AppointmentList("./test/test_input.csv")

    def test_sort_all(self):
        self.assertEqual(len(self.appointment_list.sort_all()),
                         1000,
                         "Wrong size after sort")
        self.assertListEqual([appointment.patient_id for appointment in self.appointment_list.sort_all()[:3]],
                             ["P000463", "P000710", "P000232"],
                             "Wrong order")
    
    def test_save_sorted_appointments(self):
        import csv

        self.appointment_list.save_sorted_appointments(self.appointment_list.sort_all(), "./test/temp.csv")
        with open("./test/temp.csv", mode='r') as file:
            self.assertListEqual([row["patient_id"] for row in csv.DictReader(file)][:3],
                                 ["P000463", "P000710", "P000232"],
                                 "Save Failed")

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove("./test/temp.csv")

if __name__ == "__main__":
    unittest.main()