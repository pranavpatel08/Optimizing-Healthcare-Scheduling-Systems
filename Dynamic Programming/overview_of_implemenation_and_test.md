## Implementation Flow and Testing Overview

### Implementation Flow

The **Healthcare Scheduling Optimizer** is meticulously designed to streamline the allocation of medical resources within a healthcare facility. The implementation is divided into several interconnected components, each responsible for a specific aspect of the scheduling process. Below is a detailed summary of the implementation flow:

1. **Data Handling and Preparation (`DataHandler` Class)**
   
   - **Loading Data**: The system begins by loading appointment data from an Excel file using the `DataHandler` class. This data includes crucial information such as patient IDs, scheduled dates and times, priority scores, required resources, duration of appointments, and acceptable wait times.
   
   - **Data Processing**: The `DataHandler` class processes the raw data by:
     - **Calculating Start and End Times**: Combines the scheduled date and time to create a precise `start_time` timestamp and calculates the corresponding `end_time` based on the `duration_minutes`.
     - **Sorting Data**: Organizes the appointments in chronological order, prioritizing higher priority scores to ensure that urgent cases are addressed first.
   
   - **Grouping Data**: After preparation, the data is grouped by scheduled dates to facilitate day-wise processing.

2. **Initial Room Allocation (`RoomAllocator` Class)**
   
   - **Calculating Minimum Rooms**: For each day, the `RoomAllocator` class determines the minimum number of rooms required for each room type (`TreatmentRoom`, `ConsultationRoom`, `EmergencyRoom`) to accommodate all appointments without exceeding acceptable wait times.
   
   - **Managing Room Availability**: It tracks the availability of rooms by monitoring when each room becomes free and assigns incoming appointments to available rooms accordingly.
   
   - **Wait Time Calculation**: Computes the average wait time for patients based on the room availability and their `wait_time_target`.

3. **Room Optimization (`RoomOptimizer` Class)**
   
   - **Dynamic Programming Approach**: The `RoomOptimizer` class employs a dynamic programming (DP) strategy to explore various room configurations. The goal is to find an optimal allocation that minimizes the total cost, which is a weighted sum of room usage and average wait times.
   
   - **Cost Function**: Utilizes a cost function where `alpha` represents the weight for room usage cost, and `beta` represents the weight for average wait time. The optimizer seeks to minimize this cost.
   
   - **Memoization**: Implements memoization to store and reuse previously computed configurations, enhancing the efficiency of the optimization process.

4. **Coordinator (`ScheduleOptimizerRunner` Class)**
   
   - **Orchestrating the Process**: The `ScheduleOptimizerRunner` class serves as the central coordinator, managing the entire workflow from data loading to optimization.
   
   - **Daily Processing**: For each day, it performs the following steps:
     - **Initial Allocation**: Uses the `RoomAllocator` to determine the initial room requirements and schedules.
     - **Optimization**: Invokes the `RoomOptimizer` to refine the room allocations based on the defined cost function.
     - **Recording Statistics**: Collects and stores statistics related to initial and optimized room usage, as well as wait times.
   
   - **Monthly Summary**: After processing all appointments, it generates a comprehensive summary of room usage statistics for the entire month.

### Testing Overview

To ensure the robustness and reliability of the **Healthcare Scheduling Optimizer**, a comprehensive suite of unit tests has been developed using Python’s built-in `unittest` framework. The testing strategy encompasses a wide range of scenarios to validate the system’s functionality under various conditions. Below is an overview of the testing approach and the specific test cases implemented:

1. **Test Suite Setup (`TestScheduleOptimizer` Class)**
   
   - **Temporary Environment**: Each test case operates within a temporary directory to avoid side effects and ensure isolation.
   
   - **Test Data Creation**: Utilizes helper methods to generate and save test appointment data in Excel format, simulating different scheduling scenarios.

2. **Test Cases**

   - **No Appointments (`test_no_appointments`)**
     - **Purpose**: Validates the system’s behavior when there are no appointments.
     - **Expectation**: Ensures that the system handles empty data gracefully without errors and correctly records zero room usage.
   
   - **Single Appointment (`test_single_appointment`)**
     - **Purpose**: Tests the system’s handling of a single appointment.
     - **Expectation**: Confirms that the appointment is allocated to the appropriate room without any wait time.
   
   - **Multiple Appointments at the Same Time (`test_multiple_appointments_same_time`)**
     - **Purpose**: Assesses how the system manages multiple appointments scheduled simultaneously for the same room type with varying priorities.
     - **Expectation**: Ensures that higher priority appointments are allocated first and that room limits are respected.
   
   - **Appointments Across Multiple Days (`test_appointments_across_multiple_days`)**
     - **Purpose**: Verifies the system’s capability to process appointments spanning multiple dates.
     - **Expectation**: Confirms that daily room allocations and statistics are accurately maintained without cross-day interference.
   
   - **Wait Time Edge Cases (`test_wait_time_edge_cases`)**
     - **Purpose**: Evaluates how the system handles appointments with extreme wait time targets, including zero and generous wait times.
     - **Expectation**: Ensures that appointments with zero wait time are either allocated immediately or trigger the opening of new rooms if necessary.
   
   - **Room Limits and Minimum Requirements (`test_room_limits_and_min_requirements`)**
     - **Purpose**: Tests the optimizer’s adherence to room limits while satisfying minimum room requirements.
     - **Expectation**: Validates that the system explores different room configurations to minimize costs without violating room capacity constraints.
   
   - **Realistic Sample Scenario (`test_realistic_sample_scenario`)**
     - **Purpose**: Simulates a complex and realistic set of overlapping appointments with diverse room types, durations, and priorities.
     - **Expectation**: Confirms that the system efficiently allocates rooms, minimizes wait times, and accurately calculates costs in a realistic operational context.
   
   - **Priority Handling (`test_priority_handling`)**
     - **Purpose**: Ensures that the system correctly prioritizes higher priority patients over lower priority ones when allocating rooms.
     - **Expectation**: Validates that higher priority patients experience lower wait times and are preferentially allocated available rooms.
   
   - **Consecutive Appointments (`test_consecutive_appointments`)**
     - **Purpose**: Tests the system’s ability to handle back-to-back appointments efficiently, ensuring optimal room reuse.
     - **Expectation**: Ensures that consecutive appointments are scheduled without unnecessary wait times, leveraging room availability effectively.
   
   - **Large Number of Appointments (`test_large_number_of_appointments`)**
     - **Purpose**: Assesses the system’s performance and stability when processing a large volume of appointments.
     - **Expectation**: Confirms that the system can handle high-load scenarios without degradation in performance or accuracy.
   
   - **Different Room Types (`test_different_room_types`)**
     - **Purpose**: Tests the system’s ability to manage appointments requiring different types of rooms simultaneously.
     - **Expectation**: Ensures that room allocations are handled independently per room type, maintaining separate counts and allocations.

3. **Running the Tests**

   - **Execution**: Tests can be executed using the following commands from the project root directory:
     ```bash
     python -m unittest discover -s tests
     ```
     or directly:
     ```bash
     python tests/test_scheduler.py
     ```
   
   - **Expected Outcomes**: Each test case should pass without errors, confirming that the corresponding functionality works as intended. Any failures indicate areas that may require debugging or refinement.

### Conclusion

The **Healthcare Scheduling Optimizer** efficiently manages and allocates rooms in healthcare facilities to reduce patient wait times. It uses a clear and organized approach to handle Treatment Rooms, Consultation Rooms, and Emergency Rooms. Additionally, the system includes thorough testing to ensure it works reliably in real-world situations.
