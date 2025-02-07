from Appointment import AppointmentList


def main():
    appointments = AppointmentList(
        'healthcare_scheduling_combined_view_sample_1000 1.csv')
    sorted_appointments = appointments.sort_all()

    # print first 3 appointments
    for i in range(3):
        print(sorted_appointments[i])

    # Save sorted appointments to a file
    output_file = 'sorted_appointments.csv'
    appointments.save_sorted_appointments(sorted_appointments, output_file)

    print(f"Sorted appointments saved to {output_file}")


if __name__ == "__main__":
    main()
