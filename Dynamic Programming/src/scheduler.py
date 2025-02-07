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
