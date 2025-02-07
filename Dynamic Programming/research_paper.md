# Optimizing Hospital Room Allocation: A Comparative Analysis of Two Dynamic Programming Approaches

**Group members:**
- Shanshou Li – Project Management
- Qiong Wu – Data
- Xiaohui Li, Yunyu Guo – Implementation
- Karan Kendre, Xiaowei Qi – Testing
- Ruichao Tang – Writing

**Date:** December 12, 2024

## Introduction

Hospital room allocation is a complex and critical task that directly impacts patient satisfaction, operational efficiency, and the overall quality of healthcare services. Effective scheduling ensures that patients receive timely care, reduces unnecessary wait times, and optimizes the use of available resources such as treatment, consultation, and emergency rooms. Given the dynamic nature of hospital operations, developing robust algorithms to manage room allocations is essential.

The primary objective of this project is to develop dynamic programming (DP) algorithms that reduce patient wait times, optimize doctor schedules, and improve overall hospital efficiency. Two distinct approaches have been developed, each employing different methodologies and structural designs to tackle the room allocation problem. This paper provides a comprehensive comparison of these two approaches, highlighting their unique strategies, advantages, and potential drawbacks.

## Project Background

Hospital scheduling encompasses the allocation of various types of rooms—such as Treatment, Consultation, and Emergency—to patients based on appointment schedules, room availability, patient priority, and wait time targets. The goal is to develop algorithms that dynamically assign rooms to patients in a manner that minimizes wait times, ensures high-priority patients receive timely care, and optimizes the utilization of hospital resources.

Dynamic Programming (DP) is well-suited for this problem due to its ability to break down complex optimization tasks into simpler subproblems, ensuring optimal solutions through recursive problem-solving. By leveraging DP, the project aims to create robust scheduling algorithms that can adapt to varying patient inflows and hospital capacity constraints.

## Methodology

### Approach 1: Single-Class Time-Slot-Based Dynamic Programming

The first approach is encapsulated in the `RoomAllocationSystem` class, which integrates data loading, room utilization optimization, and conflict resolution within a single structure.

#### Structure and Components

1. **Data Loading and Preparation**: Utilizes the `pandas` library to read patient data from an Excel file, randomly sampling 50 records to simulate a manageable dataset. It processes scheduled dates and times, converting them into datetime objects for easier manipulation.

2. **Dynamic Programming for Room Utilization**:
   - **Time Slot Creation**: Calculates the optimal time interval using the Greatest Common Divisor (GCD) of patient durations, ensuring a minimum interval of 5 minutes.
   - **Room Allocation**: Implements a bottom-up DP approach to allocate rooms based on availability and patient priority. It iterates through each time slot, assigning patients to available rooms while tracking utilization and handling overlaps.

3. **Conflict and Priority Handling**: Addresses overlapping appointments and priority conflicts by adjusting appointment start times and ensuring that high-priority patients are allocated rooms preferentially.

4. **Performance Metrics**: Calculates average wait times and tracks violations where actual wait times exceed target thresholds, providing insights into the efficiency of the allocation.

#### Advantages

- **Simplicity**: The integrated structure allows for straightforward implementation and understanding.
- **Focused Optimization**: Directly targets room utilization and wait time minimization within a confined framework.
- **Ease of Use**: Suitable for small-scale scenarios with limited data and room types.

#### Limitations

- **Scalability**: May struggle with larger datasets or more complex scheduling requirements due to its monolithic design.
- **Flexibility**: Limited ability to adapt to multi-day scheduling or incorporate additional constraints without significant modifications.
- **Modularity**: Lacks separation of concerns, making maintenance and extension more challenging.

### Approach 2: Modular Multi-Class Dynamic Programming with Cost Functions

The second approach is implemented through a suite of classes—`DataHandler`, `RoomAllocator`, `RoomOptimizer`, and `ScheduleOptimizerRunner`—each handling specific aspects of the scheduling problem, resulting in a highly modular and scalable system.

#### Structure and Components

1. **Data Handling** (`DataHandler`):
   - **Data Loading**: Reads and prepares data from an Excel file, ensuring comprehensive processing without random sampling.
   - **Sorting and Grouping**: Sorts appointments by date, time, and priority, and groups them by scheduled dates to facilitate multi-day scheduling.

2. **Initial Room Allocation** (`RoomAllocator`):
   - **Minimum Room Calculation**: Determines the minimum number of rooms required for each type per day using a greedy algorithm.
   - **Average Wait Time Calculation**: Computes the initial average wait times based on the room allocations.

3. **Room Optimization** (`RoomOptimizer`):
   - **Cost Function**: Introduces a cost function balancing room numbers (`alpha`) and average wait times (`beta`), allowing for flexible optimization based on hospital priorities.
   - **Dynamic Programming**: Employs a recursive DP approach to evaluate different room configurations, seeking to minimize the total cost by adjusting room allocations.

4. **Scheduling and Reporting** (`ScheduleOptimizerRunner`):
   - **Coordination**: Manages the overall process, coordinating data handling, initial allocation, and optimization.
   - **Monthly Statistics**: Aggregates and summarizes room usage statistics over a monthly period, providing insights into average, maximum, and minimum room requirements.
   - **Detailed Reporting**: Utilizes the `tabulate` library to present allocation results in a readable tabular format.

#### Advantages

- **Modularity**: Clear separation of concerns across multiple classes enhances maintainability and scalability.
- **Flexibility**: Capable of handling multi-day scheduling and adjusting room allocations dynamically based on varying demands.
- **Comprehensive Optimization**: Incorporates cost functions to balance room availability with wait time minimization, allowing for more nuanced scheduling decisions.
- **Detailed Reporting**: Provides extensive statistical summaries, aiding in informed decision-making and long-term planning.

#### Limitations

- **Complexity**: The multi-class structure introduces complexity, which may require more effort to implement and understand.
- **Performance**: Recursive DP with extensive cost evaluations may be computationally intensive, particularly with large datasets.
- **Parameter Sensitivity**: The effectiveness of the cost function depends on the appropriate tuning of `alpha` and `beta` parameters, which may require empirical adjustments.

## Results and Discussion

### Performance Comparison

| **Metric**                       | **Approach 1**                                      | **Approach 2**                                                   |
|----------------------------------|-----------------------------------------------------|------------------------------------------------------------------|
| **Average Wait Time**            | Calculated per day                                  | Calculated per day and optimized monthly                        |
| **Room Utilization**             | High within limited scope                           | Balanced across multiple days                                   |
| **Scalability**                  | Limited to small datasets                           | Scalable to larger datasets and multi-day scheduling            |
| **Flexibility in Optimization**  | Limited to room utilization and wait time           | Flexible with cost functions balancing room numbers and wait times |
| **Reporting and Insights**       | Basic performance metrics                           | Detailed monthly statistics and tabulated reports               |
| **Implementation Complexity**    | Simple and straightforward                         | Complex due to modular structure                                |

### Analysis

**Approach 1** demonstrates effectiveness in optimizing room utilization and minimizing wait times within a confined, single-day framework. Its simplicity facilitates easy implementation and quick results for small-scale scenarios. However, its lack of modularity and flexibility limits its applicability in more complex, real-world settings where multi-day scheduling and dynamic adjustments are essential.

**Approach 2**, with its modular design and incorporation of cost functions, offers a more robust and scalable solution. It effectively balances room availability with wait time minimization across multiple days, providing comprehensive statistical insights that are valuable for long-term planning. The flexibility to adjust optimization parameters (`alpha` and `beta`) allows for tailored scheduling strategies based on specific hospital priorities. Nonetheless, the increased complexity and computational demands pose challenges, particularly in large-scale implementations.

### Practical Implications

The choice between these two approaches depends largely on the specific needs and scale of the hospital's scheduling requirements:

- **Small to Medium Hospitals**: Approach 1 may suffice, offering a straightforward method to optimize room allocation without the overhead of managing multiple classes and complex algorithms.

- **Large Hospitals or Multi-Day Scheduling**: Approach 2 is more suitable, providing the necessary scalability and flexibility to handle extensive scheduling demands and dynamic resource management.

## Conclusion

This comparative study highlights the distinct methodologies and strategic differences between two dynamic programming approaches to hospital room allocation. **Approach 1** offers simplicity and efficiency within a limited scope, making it suitable for smaller-scale applications. In contrast, **Approach 2** provides a comprehensive, scalable, and flexible framework capable of addressing the complexities of multi-day scheduling and varied hospital demands. Ultimately, the selection of an appropriate algorithm depends on the specific operational requirements, data scale, and desired flexibility of the hospital's scheduling system. 

---

## Appendix

### Approach 1: Single-Class Time-Slot-Based Dynamic Programming

```python
"""
Hospital Room Allocation System

This script implements a room allocation system that:
1. Reads patient data from an Excel file
2. Allocates rooms based on priority and wait times
3. Aims to minimize average wait time while respecting priority scores
4. Handles three types of rooms: Treatment, Consultation, and Emergency
"""

import pandas as pd
from typing import List
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Patient:
    """
    Patient data structure containing all relevant information for room allocation

    Attributes:
        id: Unique patient identifier (e.g., P000666)
        scheduled_datetime: When the patient is scheduled for
        duration_minutes: How long they need the room
        required_resources: Type of room needed (Treatment/Consultation/Emergency)
        priority_score: Higher score means higher priority (1-100)
        condition_type: Emergency, Urgent, or Routine
        wait_time_target: Maximum acceptable wait time in minutes
    """
    id: str
    scheduled_datetime: datetime
    duration_minutes: int
    required_resources: str
    priority_score: int
    condition_type: str
    wait_time_target: int

class RoomAllocationSystem:
    def __init__(self, total_rooms: int):
        """
        Initialize room allocation system

        Strategy:
        - Divide total rooms equally among three types
        - Ensure at least 1 room of each type
        - Any remaining rooms go to emergency

        Args:
            total_rooms: Total number of rooms available
        """
        self.total_rooms = total_rooms
        # Split rooms equally (minimum 1 per type), Any remaining rooms go to emergency
        self.treatment_rooms = max(1, total_rooms // 3)
        self.consultation_rooms = max(1, total_rooms // 3)
        self.emergency_rooms = total_rooms - self.treatment_rooms - self.consultation_rooms

        self.room_availability = None

    def load_patient_data(self, excel_file: str) -> List[Patient]:
        """
        Load and parse patient data from Excel file

        Args:
            excel_file: Path to Excel file containing patient data

        Returns:
            List of Patient objects with parsed data
        """
        # Read Excel file
        df = pd.read_excel(excel_file)
        # Randomly sample 50 rows
        df = df.sample(n=50, random_state=42)
        print("\nExcel Sheet Information:")
        print(df.info())
        print("\nFirst few rows of data:")
        print(df.head())

        # Convert date and time columns to datetime
        df['scheduled_datetime'] = pd.to_datetime(
            df['scheduled_date'].astype(str) + ' ' + df['scheduled_time'].astype(str)
        )

        # Get the earliest scheduled time from the data
        earliest_time = df['scheduled_datetime'].min()

        # Initialize room availability with earliest scheduled time
        self.room_availability = {
            'TreatmentRoom': [earliest_time] * self.treatment_rooms,
            'ConsultationRoom': [earliest_time] * self.consultation_rooms,
            'EmergencyRoom': [earliest_time] * self.emergency_rooms
        }

        patients = []
        for _, row in df.iterrows():
            # Extract room type from required_resources (first part before comma)
            room_type = row['required_resources'].split(',')[0]

            # Create Patient object
            patient = Patient(
                id=row['patient_id'],
                scheduled_datetime=row['scheduled_datetime'],
                duration_minutes=row['duration_minutes'],
                required_resources=room_type,
                priority_score=row['priority_score'],
                condition_type=row['condition_type'],
                wait_time_target=row['wait_time_target']
            )
            patients.append(patient)
        return patients

    def get_optimal_interval(self, patients: List[Patient]) -> int:
        """Calculate smallest practical interval using GCD: Greatest Common Divisor"""
        # Get all unique durations
        durations = set(p.duration_minutes for p in patients)

        # Calculate GCD of all durations
        from math import gcd
        from functools import reduce
        optimal_interval = reduce(gcd, durations)

        # Ensure minimum 5-minute interval
        return max(5, optimal_interval)

    def create_time_slots(self, start_time: datetime, end_time: datetime, interval: int):
        """Create time slots using optimal interval"""
        time_slots = []
        current = start_time
        while current <= end_time:
            time_slots.append(current)
            current += timedelta(minutes=interval)
        return time_slots

    def optimize_room_utilization(self, time_slots: List[datetime], patients: List[Patient]):
        """Bottom-up DP for room utilization optimization"""
        # Initialize DP table
        dp = {}  # [time_index][room_state] -> (utilization, allocations)

        for t in range(len(time_slots)):
            dp[t] = {}
            for room_type in self.room_availability:
                for room_num in range(len(self.room_availability[room_type])):
                    room_key = (room_type, room_num)
                    dp[t][room_key] = {
                        'utilization': 0.0,
                        'allocations': [],
                        'end_time': time_slots[t]
                    }

        # Fill DP table bottom-up
        for t in range(len(time_slots)):
            current_time = time_slots[t]

            # Get available patients
            available_patients = [
                p for p in patients
                if p.scheduled_datetime <= current_time and
                not any(p.id in alloc['patient_id']
                        for prev_t in range(t)
                        for room in dp[prev_t].values()
                        for alloc in room['allocations'])
            ]

            # For each room
            for room_key in dp[t]:
                room_type, room_num = room_key

                # Get matching patients for this room type
                matching_patients = [
                    p for p in available_patients
                    if p.required_resources == room_type
                ]

                # Try each patient
                best_utilization = 0
                best_allocation = None

                for patient in matching_patients:
                    # Calculate room utilization with this patient
                    duration = patient.duration_minutes
                    # time_slot_length = (next_time - current_time)
                    utilization = duration / (time_slots[t+1] - current_time).total_seconds() * 60 if t < len(time_slots)-1 else 1

                    if utilization > best_utilization:
                        best_utilization = utilization
                        best_allocation = {
                            'patient_id': patient.id,
                            'start_time': current_time,
                            'end_time': current_time + timedelta(minutes=duration),
                            'room_type': room_type,
                            'room_number': room_num,
                            'priority_score': patient.priority_score,
                            'wait_time_target': patient.wait_time_target,
                            'duration_minutes': patient.duration_minutes
                        }

                # Update DP table
                if best_allocation:
                    dp[t][room_key]['utilization'] = best_utilization
                    dp[t][room_key]['allocations'].append(best_allocation)
                    dp[t][room_key]['end_time'] = best_allocation['end_time']

        # Combines all allocations from different time slots and rooms into a single list
        final_allocations = []
        for t in range(len(time_slots)):
            for room_key in dp[t]:
                final_allocations.extend(dp[t][room_key]['allocations'])

        return final_allocations

    def handle_edge_cases(self, time_slots: List[datetime], initial_allocations: List[dict]):
        """Bottom-up DP for handling edge cases"""
        # Initialize DP table
        dp = {}  # [time_index][conflict_state] -> (resolved_allocations)

        for t in range(len(time_slots)):
            dp[t] = {
                'no_conflict': [],
                'overlap_resolved': [],
                'priority_resolved': []
            }

        # Get allocations for this time slot
        def get_time_slot_allocations(time: datetime, allocations: List[dict]) -> List[dict]:
            return [a for a in allocations
                    if a['start_time'] <= time < a['end_time']]

        # Fill DP table bottom-up
        for t in range(len(time_slots)):
            current_time = time_slots[t]
            current_allocations = get_time_slot_allocations(
                current_time,
                initial_allocations
            )

            # Handle overlapping appointments
            def resolve_overlaps(allocations: List[dict]) -> List[dict]:
                resolved = []
                delayed = []

                # Sorting logic: Higher priority scores come first; when priority scores are equal, earlier times come first
                for alloc in sorted(allocations,
                                key=lambda x: (x['priority_score'], x['start_time']),
                                reverse=True):
                    # Check for overlap with resolved allocations
                    overlap = False
                    for res in resolved:
                        if (alloc['start_time'] < res['end_time'] and # 1. New appointment starts before existing appointment ends
                            alloc['end_time'] > res['start_time'] and # 2. New appointment ends after existing appointment starts
                            alloc['room_type'] == res['room_type'] and # 3. appointments are in the same room type
                            alloc['room_number'] == res['room_number']): # 4. appointments are in the same room number
                            overlap = True
                            break

                    if not overlap:
                        resolved.append(alloc)
                    else:
                        # Delay overlapping appointment
                        delayed.append({
                            **alloc,  # Copy all original appointment details
                            'start_time': max(r['end_time'] for r in resolved
                                            if r['room_type'] == alloc['room_type']), # Set new start time to latest end time for this room type
                            'end_time': max(r['end_time'] for r in resolved
                                        if r['room_type'] == alloc['room_type']) +
                                    timedelta(minutes=alloc['duration_minutes'])
                        })

                return resolved + delayed

            # Handle priority conflicts
            def resolve_priority_conflicts(allocations: List[dict]) -> List[dict]:
                # Calculate combined priority for each allocation: higher priority_score and lower wait_time_target has higher priority
                for alloc in allocations:
                    alloc['combined_priority'] = alloc['priority_score'] / alloc['wait_time_target']

                # Sort by combined priority (higher is better)
                return sorted(
                    allocations,
                    key=lambda x: x['combined_priority'],
                    reverse=True
                )

            # Resolve overlaps
            dp[t]['overlap_resolved'] = resolve_overlaps(current_allocations)
            # Resolve priority conflicts
            dp[t]['priority_resolved'] = resolve_priority_conflicts(
                dp[t]['overlap_resolved']
            )

        # Combine resolved allocations
        final_allocations = []
        for t in range(len(time_slots)):
            final_allocations.extend(dp[t]['priority_resolved'])

        return sorted(final_allocations, key=lambda x: x['start_time'])

    def allocate_rooms_complete(self, patients: List[Patient]):
        """Complete room allocation with all optimizations"""
        # 1. Get optimal interval
        interval = self.get_optimal_interval(patients)

        # 2. Create time slots
        time_slots = self.create_time_slots(
            min(p.scheduled_datetime for p in patients),
            max(p.scheduled_datetime + timedelta(minutes=p.duration_minutes)
                for p in patients),
            interval
        )

        # 3. Initial allocation with room utilization optimization
        initial_allocations = self.optimize_room_utilization(
            time_slots,
            patients
        )

        # 4. Handle edge cases
        resolved_allocations = self.handle_edge_cases(
            time_slots,
            initial_allocations
        )

        # 5. Calculate actual wait times and add to allocations
        final_allocations = []
        for alloc in resolved_allocations:
            # Find original patient data
            patient = next(p for p in patients if p.id == alloc['patient_id'])

            # Calculate actual wait time
            actual_wait_time = (alloc['start_time'] - patient.scheduled_datetime).total_seconds() / 60

            # Add wait time information
            final_allocation = {
                **alloc,
                'actual_wait_time': actual_wait_time,
                'target_wait_time': patient.wait_time_target,
                'priority_score': patient.priority_score
            }
            final_allocations.append(final_allocation)

        return final_allocations

def main():
    """
    Main execution flow:
    1. Get number of rooms from user
    2. Initialize allocation system
    3. Load patient data
    4. Perform allocation
    5. Display results and statistics
    """
    # Get and validate room count
    while True:
        try:
            n = int(input("Enter the total number of available rooms: "))
            if n < 3:
                print("Minimum 3 rooms required")
                continue
            break
        except ValueError:
            print("Please enter a valid number")

    system = RoomAllocationSystem(n)

    # Load and process patient data
    try:
        patients = system.load_patient_data('healthcare_scheduling_combined_view_sample_1000.xlsx')
    except FileNotFoundError:
        print("Error: healthcare_scheduling_combined_view_sample_1000.xlsx not found")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Perform room allocation
    allocations = system.allocate_rooms_complete(patients)

    # Display results
    print("\nRoom Allocation Results:")
    print(f"Total Rooms: {n}")
    print(f"Treatment Rooms: {system.treatment_rooms}")
    print(f"Consultation Rooms: {system.consultation_rooms}")
    print(f"Emergency Rooms: {system.emergency_rooms}")

    # Calculate and display statistics
    total_wait_time = 0
    violations = 0

    # Use a set to track displayed allocations
    displayed_allocations = set()

    # Display results
    print("\nDetailed Allocation Results:")
    for allocation in sorted(allocations, key=lambda x: x['start_time']):
        # Create a unique key for this allocation
        alloc_key = (allocation['patient_id'], allocation['start_time'])

        if alloc_key not in displayed_allocations:
            displayed_allocations.add(alloc_key)

            print(f"\nPatient ID: {allocation['patient_id']}")
            print(f"Room Type: {allocation['room_type']}")
            print(f"Room Number: {allocation['room_number']}")
            print(f"Start Time: {allocation['start_time']}")
            print(f"End Time: {allocation['end_time']}")
            print(f"Actual Wait Time: {allocation['actual_wait_time']:.0f} minutes")
            print(f"Target Wait Time: {allocation['target_wait_time']} minutes")

            # Track statistics
            total_wait_time += allocation['actual_wait_time']
            if allocation['actual_wait_time'] > allocation['target_wait_time']:
                violations += 1

    # Display performance metrics
    if displayed_allocations:  # Check if we have any allocations
        avg_wait_time = total_wait_time / len(displayed_allocations)
        print(f"\nPerformance Metrics:")
        print(f"Average Wait Time: {avg_wait_time:.1f} minutes")
        print(f"Wait Time Target Violations: {violations}")

if __name__ == "__main__":
    main()
```

### Approach 2: Modular Multi-Class Dynamic Programming with Cost Functions

```python
import pandas as pd
from datetime import timedelta
from tabulate import tabulate

class DataHandler:
    """Handles data loading, sorting, and preparation."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_and_prepare_data(self):
        """Loads and sorts data by scheduled date, start time, and priority score."""
        self.data = pd.read_excel(self.file_path)
        self.data['start_time'] = pd.to_datetime(
            self.data['scheduled_date'].astype(str) + ' ' + self.data['scheduled_time'].astype(str)
        )
        self.data['end_time'] = self.data['start_time'] + pd.to_timedelta(self.data['duration_minutes'], unit='m')
        self.data = self.data.sort_values(
            by=['scheduled_date', 'start_time', 'priority_score'],
            ascending=[True, True, False]
        )
        return self.data

    def group_data_by_date(self):
        """Groups the prepared data by scheduled date."""
        return self.data.groupby(self.data['scheduled_date'])

class RoomAllocator:
    """Calculates initial room requirements and average wait times."""

    def __init__(self, appointments):
        self.appointments = appointments

    def calculate_min_rooms_for_day(self):
        """Calculate minimum rooms needed for the day and average wait time."""
        rooms = {
            'TreatmentRoom': [],
            'ConsultationRoom': [],
            'EmergencyRoom': []
        }

        max_rooms_needed = {
            'TreatmentRoom': 0,
            'ConsultationRoom': 0,
            'EmergencyRoom': 0
        }

        total_wait_time = 0.0
        total_patients = 0
        schedule = []

        for _, appointment in self.appointments.iterrows():
            room_type = appointment['required_resources'].split(',')[0]
            scheduled_start_time = appointment['start_time']
            duration = appointment['duration_minutes']
            wait_time_target = appointment['wait_time_target']
            patient_id = appointment['patient_id']

            # Clean up finished appointments (rooms free before scheduled_start_time)
            rooms[room_type] = [end for end in rooms[room_type] if end > scheduled_start_time]

            if not rooms[room_type]:
                # No rooms currently in use, no wait
                actual_start_time = scheduled_start_time
                actual_end_time = actual_start_time + timedelta(minutes=duration)
                wait_time = 0.0
                rooms[room_type].append(actual_end_time)
            else:
                # Rooms are in use, find the earliest end time
                earliest_end = min(rooms[room_type])
                if earliest_end <= scheduled_start_time:
                    # Earliest room finishes before or exactly at the start time, no wait
                    actual_start_time = scheduled_start_time
                    actual_end_time = actual_start_time + timedelta(minutes=duration)
                    wait_time = 0.0

                    rooms[room_type].remove(earliest_end)
                    rooms[room_type].append(actual_end_time)
                else:
                    # Need to wait until the earliest room finishes
                    wait_time = (earliest_end - scheduled_start_time).total_seconds() / 60.0
                    if wait_time <= wait_time_target:
                        # Acceptable wait, use the same room
                        actual_start_time = earliest_end
                        actual_end_time = actual_start_time + timedelta(minutes=duration)

                        rooms[room_type].remove(earliest_end)
                        rooms[room_type].append(actual_end_time)
                    else:
                        # Exceeds acceptable wait, open a new room
                        actual_start_time = scheduled_start_time
                        actual_end_time = actual_start_time + timedelta(minutes=duration)
                        rooms[room_type].append(actual_end_time)
                        wait_time = 0.0  # Reset wait_time since a new room is opened

            # Update maximum room usage
            max_rooms_needed[room_type] = max(max_rooms_needed[room_type], len(rooms[room_type]))

            total_wait_time += wait_time
            total_patients += 1

            schedule.append({
                'Patient ID': patient_id,
                'Room Type': room_type,
                'Start Time': actual_start_time,
                'End Time': actual_end_time,
                'Wait Time': wait_time
            })

        # Calculate average wait time
        average_wait_time = total_wait_time / total_patients if total_patients > 0 else 0.0
        return max_rooms_needed, average_wait_time, schedule

class RoomOptimizer:
    """Optimizes room allocations with a cost function using dynamic programming."""

    def __init__(self, appointments, room_limits, min_rooms_required, alpha=1.0, beta=2.0):
        self.appointments = appointments
        self.room_limits = room_limits
        self.min_rooms_required = min_rooms_required
        self.alpha = alpha
        self.beta = beta
        self.memo = {}

    def calculate_cost(self, room_config, average_wait_time):
        """Calculate the cost based on room usage and average wait time."""
        total_room_cost = sum(room_config.values())
        return self.alpha * total_room_cost + self.beta * average_wait_time

    def dp(self, room_config):
        """Dynamic programming approach to evaluate a given room configuration."""
        config_key = tuple(sorted(room_config.items()))
        if config_key in self.memo:
            return self.memo[config_key]

        # Simulate scheduling based on the current configuration
        rooms = {rtype: [pd.Timestamp.min] * count for rtype, count in room_config.items()}
        total_wait_time = 0
        total_patients = 0
        schedule = []

        for _, appointment in self.appointments.iterrows():
            room_type = appointment['required_resources'].split(',')[0]
            scheduled_start_time = appointment['start_time']
            duration = appointment['duration_minutes']
            wait_time_target = appointment['wait_time_target']
            patient_id = appointment['patient_id']

            # Remove finished appointments
            rooms[room_type] = [end for end in rooms[room_type] if end > scheduled_start_time]

            if len(rooms[room_type]) < room_config[room_type]:
                # There is a free room, no wait
                actual_start_time = scheduled_start_time
                wait_time = 0.0
            else:
                # No free room, must wait for the earliest ending room
                earliest_end = min(rooms[room_type])
                wait_time = (earliest_end - scheduled_start_time).total_seconds() / 60.0

                if wait_time <= wait_time_target:
                    # Acceptable wait, use the same room
                    actual_start_time = earliest_end
                    rooms[room_type].remove(earliest_end)
                else:
                    # Exceeds acceptable wait, cannot add rooms in DP, must wait anyway
                    actual_start_time = earliest_end
                    wait_time = (actual_start_time - scheduled_start_time).total_seconds() / 60.0

            actual_end_time = actual_start_time + timedelta(minutes=duration)
            rooms[room_type].append(actual_end_time)

            # Update totals
            total_wait_time += wait_time
            total_patients += 1

            # Add to schedule with wait time for debugging
            schedule.append({
                'Patient ID': patient_id,
                'Room Type': room_type,
                'Start Time': actual_start_time,
                'End Time': actual_end_time,
                'Wait Time': wait_time
            })

        # Calculate the average wait time
        average_wait_time = total_wait_time / total_patients if total_patients else 0
        cost = self.calculate_cost(room_config, average_wait_time)

        self.memo[config_key] = (cost, average_wait_time, schedule)
        return cost, average_wait_time, schedule

    def find_optimal_config(self, current_config, depth=0):
        """Recursively find the optimal room configuration."""
        if depth == len(self.room_limits):
            return self.dp(current_config), current_config

        room_type = list(self.room_limits.keys())[depth]
        best_cost = float('inf')
        best_config = None
        best_avg_wait = float('inf')
        best_schedule = []

        min_room_count = self.min_rooms_required[room_type]
        max_room_count = self.room_limits[room_type]

        # Ensure that min_room_count does not exceed max_room_count
        if min_room_count > max_room_count:
            # No valid configuration for this room type
            return (float('inf'), float('inf'), []), None

        for i in range(min_room_count, max_room_count + 1):
            current_config[room_type] = i
            (cost, avg_wait, schedule), config = self.find_optimal_config(dict(current_config), depth + 1)
            if config is None:
                continue  # Skip invalid configurations
            if cost < best_cost:
                best_cost = cost
                best_avg_wait = avg_wait
                best_config = config
                best_schedule = schedule

        return (best_cost, best_avg_wait, best_schedule), best_config

    def optimize_rooms(self):
        """Optimize room allocation starting from the minimum required rooms."""
        initial_config = self.min_rooms_required.copy()  # Ensure a copy is made
        return self.find_optimal_config(initial_config)

class ScheduleOptimizerRunner:
    """Coordinates the data processing, initial calculations, and room optimization."""

    def __init__(self, file_path, room_limits, alpha=1.0, beta=2.0):
        self.file_path = file_path
        self.room_limits = room_limits
        self.alpha = alpha
        self.beta = beta
        self.monthly_stats_initial = {'TreatmentRoom': [], 'ConsultationRoom': [], 'EmergencyRoom': []}
        self.monthly_stats_optimized = {'TreatmentRoom': [], 'ConsultationRoom': [], 'EmergencyRoom': []}

    def run(self):
        # Load and prepare data
        data_handler = DataHandler(self.file_path)
        data = data_handler.load_and_prepare_data()
        grouped_data = data_handler.group_data_by_date()

        # Define room order for sorting schedules
        room_order = {'ConsultationRoom': 0, 'TreatmentRoom': 1, 'EmergencyRoom': 2}

        # Process each day
        for day, group in grouped_data:
            print(f"Processing date: {day.date()}")

            # Calculate initial room requirements
            allocator = RoomAllocator(group)
            min_rooms, avg_wait_initial, initial_schedule = allocator.calculate_min_rooms_for_day()
            initial_cost = sum(min_rooms.values()) + self.beta * avg_wait_initial

            # Sort initial schedule by Room Type in desired order
            initial_schedule.sort(key=lambda x: room_order.get(x['Room Type'], 99))

            print(f"Initial Allocation: Rooms - {min_rooms}, Cost: {initial_cost:.2f}, Average Wait Time: {avg_wait_initial:.2f} minutes")
            print(f"Initial Schedule:\n{tabulate(initial_schedule, headers='keys', tablefmt='grid')}")

            # Record initial stats
            for room_type, count in min_rooms.items():
                self.monthly_stats_initial[room_type].append(count)

            # Optimize room allocation
            optimizer = RoomOptimizer(group, self.room_limits, min_rooms, self.alpha, self.beta)
            optimization_result = optimizer.optimize_rooms()

            if optimization_result is None:
                print("No valid room configuration found within the given room limits and constraints.")
                print('---------------------------')
                continue  # Skip recording optimized stats

            (optimal_cost, optimal_avg_wait, optimized_schedule), optimal_rooms = optimization_result

            if optimal_rooms is None:
                print("No valid room configuration found within the given room limits and constraints.")
                print('---------------------------')
                continue  # Skip recording optimized stats

            # Sort optimized schedule by Room Type in desired order
            optimized_schedule.sort(key=lambda x: room_order.get(x['Room Type'], 99))

            print(f"Optimized Allocation: Rooms - {optimal_rooms}, Cost: {optimal_cost:.2f}, Average Wait Time: {optimal_avg_wait:.2f} minutes")
            print(f"Optimized Schedule:\n{tabulate(optimized_schedule, headers='keys', tablefmt='grid')}")

            # Record optimized stats
            for room_type, count in optimal_rooms.items():
                self.monthly_stats_optimized[room_type].append(count)

            print('---------------------------')

        self.summarize_month()

    def summarize_month(self):
        """Summarize the stats for the entire month."""
        print("Monthly Summary (Initial Allocation):")
        self.print_monthly_stats(self.monthly_stats_initial)

        print("\nMonthly Summary (Wait-Minimized Allocation):")
        self.print_monthly_stats(self.monthly_stats_optimized)

    def print_monthly_stats(self, stats_dict):
        for room_type, counts in stats_dict.items():
            avg = sum(counts) / len(counts) if counts else 0
            max_count = max(counts) if counts else 0
            min_count = min(counts) if counts else 0
            print(f"{room_type}: Average: {avg:.2f}, Max: {max_count}, Min: {min_count}")

if __name__ == "__main__":
    # Define room limits (maximum rooms available for each type)
    room_limits = {
        'TreatmentRoom': 10,
        'ConsultationRoom': 10,
        'EmergencyRoom': 10
    }

    # Initialize and run the scheduler
    runner = ScheduleOptimizerRunner('healthcare_scheduling_combined_view_sample_1000.xlsx', room_limits, alpha=1.0, beta=2.0)
    runner.run()
```