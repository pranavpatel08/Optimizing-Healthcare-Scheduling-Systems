# Healthcare Scheduling Optimizer

## Introduction

The **Healthcare Scheduling Optimizer** is a collaborative project of CS 5800 designed to optimize room allocation within healthcare facilities. By efficiently managing resources such as Treatment Rooms, Consultation Rooms, and Emergency Rooms, the system aims to minimize patient waiting times and enhance the overall efficiency of medical services. This optimization not only improves patient satisfaction but also ensures the optimal utilization of medical resources.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Preparing Data](#preparing-data)
  - [Running the Optimizer](#running-the-optimizer)
- [Testing](#testing)
- [Classes and Functionalities](#classes-and-functionalities)
  - [DataHandler](#datahandler)
  - [RoomAllocator](#roomallocator)
  - [RoomOptimizer](#roomoptimizer)
  - [ScheduleOptimizerRunner](#scheduleoptimizerrunner)
- [Testing Scenarios](#testing-scenarios)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Structure

```
healthcare_scheduling_project/
├── src/
│   ├── __init__.py
│   └── scheduler.py
├── tests/
│   ├── __init__.py
│   └── test_scheduler.py
├── requirements.txt
├── README.md
└── .gitignore
```

- **`src/`**: Contains the implementation code.
  - **`scheduler.py`**: Main module with core classes and functionalities.
- **`tests/`**: Contains the test code.
  - **`test_scheduler.py`**: Unit tests for the scheduler.
- **`requirements.txt`**: Lists the project dependencies.
- **`README.md`**: Project documentation.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.

## Installation

### Prerequisites

- **Python 3.7+**
- **pip**

### Clone the Repository

```bash
git clone https://github.com/pranavpatel08/Optimizing-Healthcare-Scheduling-Systems.git
cd Optimizing-Healthcare-Scheduling-Systems
```

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

### Preparing Data

Prepare your appointment data in an Excel file with the following columns:

- **`patient_id`**: Patient identifier.
- **`scheduled_date`**: Appointment date (format: `YYYY-MM-DD`).
- **`scheduled_time`**: Appointment time (format: `HH:MM:SS`).
- **`priority_score`**: Priority score (higher values indicate higher priority).
- **`required_resources`**: Required resource type (e.g., `TreatmentRoom`, `ConsultationRoom`, `EmergencyRoom`).
- **`duration_minutes`**: Duration of the appointment in minutes.
- **`wait_time_target`**: Acceptable wait time in minutes.

### Running the Optimizer

1. **Edit Implementation Code**

   In `src/scheduler.py`, ensure the data file path and room limits are correctly set. For example:

   ```python
   # src/scheduler.py

   from scheduler import ScheduleOptimizerRunner

   # Define room limits
   room_limits = {
       'TreatmentRoom': 10,
       'ConsultationRoom': 10,
       'EmergencyRoom': 5
   }

   # Initialize the runner and execute the optimization
   runner = ScheduleOptimizerRunner(
       'path_to_your_excel_file.xlsx', 
       room_limits,
       alpha=1.0,
       beta=2.0
   )
   runner.run()
   ```

   - **`alpha`**: Weight for room usage cost.
   - **`beta`**: Weight for average wait time cost.

2. **Run the Script**

   In the terminal, navigate to the project root directory and execute:

   ```bash
   python src/scheduler.py
   ```

   The script will load the data, calculate initial room requirements, optimize room allocations, and output daily allocations along with monthly statistics.

## Testing

The test code is located in `tests/test_scheduler.py`. Ensure that `unittest` is available (it is included in Python’s standard library).

### Running Tests

Run all test cases using the following command in the project root directory:

```bash
python -m unittest discover -s tests
```

Alternatively, directly run the test script:

```bash
python tests/test_scheduler.py
```

## Classes and Functionalities

### DataHandler

Handles loading and preparing the appointment data.

- **`__init__(self, file_path)`**: Initializes the data handler with the specified Excel file path.
- **`load_and_prepare_data(self)`**: Loads data from the Excel file, calculates start and end times for appointments, and sorts the data by date, time, and priority score.
- **`group_data_by_date(self)`**: Groups the data by scheduled date.

### RoomAllocator

Calculates the minimum number of rooms needed for a day and the average wait time.

- **`__init__(self, appointments)`**: Initializes the allocator with daily appointments data.
- **`calculate_min_rooms_for_day(self)`**: Computes the required number of rooms, average wait time, and schedule based on the appointments.

### RoomOptimizer

Optimizes room allocations using dynamic programming to minimize total cost, which includes room usage and wait time.

- **`__init__(self, appointments, room_limits, min_rooms_required, alpha=1.0, beta=2.0)`**: Initializes the optimizer with appointments data, room limits, minimum rooms required, and cost parameters.
- **`optimize_rooms(self)`**: Starts the optimization process to find the optimal room configuration.
- **`find_optimal_config(self, current_config, depth=0)`**: Recursively searches for the optimal room configuration.
- **`dp(self, room_config)`**: Evaluates a given room configuration using dynamic programming.

### ScheduleOptimizerRunner

Coordinates data processing, initial calculations, and room optimization.

- **`__init__(self, file_path, room_limits, alpha=1.0, beta=2.0)`**: Initializes the runner with the data file path, room limits, and cost parameters.
- **`run(self)`**: Main method that processes each day’s appointments, calculates initial and optimized room allocations, and records statistics.
- **`summarize_month(self)`**: Summarizes and prints monthly statistics.
- **`print_monthly_stats(self, stats_dict)`**: Prints statistical data including averages, maxima, and minima for room usage.

## Testing Scenarios

The test suite covers various scenarios to ensure the system's robustness and correctness:

1. **No Appointments (`test_no_appointments`)**:
   - Tests the system's behavior with no appointments, ensuring no errors occur and statistics are correctly recorded.

2. **Single Appointment (`test_single_appointment`)**:
   - Tests room allocation and wait time calculation with a single appointment.

3. **Multiple Appointments at the Same Time (`test_multiple_appointments_same_time`)**:
   - Tests how the system handles multiple appointments scheduled simultaneously for the same room type with different priorities.

4. **Appointments Across Multiple Days (`test_appointments_across_multiple_days`)**:
   - Tests the system's ability to process appointments spanning multiple dates.

5. **Wait Time Edge Cases (`test_wait_time_edge_cases`)**:
   - Tests appointments with varying wait time targets, including zero and generous values.

6. **Room Limits and Minimum Requirements (`test_room_limits_and_min_requirements`)**:
   - Tests the optimizer's ability to respect room limits and optimize configurations accordingly.

7. **Realistic Sample Scenario (`test_realistic_sample_scenario`)**:
   - Tests the system with a complex set of overlapping appointments of different types, durations, and priorities.

8. **Priority Handling (`test_priority_handling`)**:
   - Tests whether higher priority patients are allocated rooms first.

9. **Consecutive Appointments (`test_consecutive_appointments`)**:
   - Tests efficient room reuse with back-to-back appointments.

10. **Large Number of Appointments (`test_large_number_of_appointments`)**:
    - Tests system performance and stability with a large dataset.


## Contact

For any questions or suggestions, please contact me:

- **Email**: patel.pranav2@northeastern.edu
- **GitHub**: [pranavpatel08](https://github.com/pranavpatel08)