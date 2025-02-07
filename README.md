# Healthcare Scheduling Optimization System

An advanced healthcare scheduling system that optimizes patient flow, resource allocation, and waiting times using sorting algorithms, dynamic programming, and graph theory.

## Features

- **Multi-level Patient Prioritization**
  - Condition-based sorting (Emergency, Urgent, Routine)
  - Priority score calculation
  - Wait time optimization

- **Resource Allocation**
  - Dynamic doctor efficiency tracking
  - Room utilization optimization
  - Cleaning time management

- **Schedule Optimization**
  - Daily and monthly scheduling
  - Conflict resolution
  - Real-time adjustments

## System Components

### Sorting Module
- Implements multi-tiered sorting for patient prioritization
- Handles priority scores and wait time targets
- Maintains queue management

### Dynamic Programming Module
- Optimizes daily scheduling operations
- Implements monthly resource allocation
- Manages conflict resolution

### Graph Theory Module
- Optimizes patient flow using A* pathfinding
- Tracks resource efficiency
- Manages doctor workload distribution

## Installation

```
git clone https://github.com/pranavpatel08/Optimizing-Healthcare-Scheduling-Systems.git
cd Optimizing-Healthcare-Scheduling-Systems
pip install -r requirements.txt
```

## Implementation

### Directory Structure
```
healthcare-scheduling/
├── src/
│ ├── Sorting/
│ ├── Dynamic Programming/
│ ├── Graph/
└── docs/
```

## Data Schema

### Patient Data
- patient_id: Unique identifier (Format: P000XXX)
- scheduled_date: Appointment date (YYYY-MM-DD)
- scheduled_time: Time slot (HH:MM)
- duration_minutes: Appointment duration
- priority_score: 80±10 (Emergency), 60±10 (Urgent), 40±10 (Routine)
- condition_type: Emergency/Urgent/Routine

### Resource Data
- room_id: Unique room identifier
- doctor_id: Unique doctor identifier
- efficiency_score: Current doctor efficiency
- availability: Time slots available

### Mathematical Models

#### Doctor Efficiency
The efficiency model is defined as:
\[ E_d = E_b - (P_o + P_r + P_p + W_d) \]

where:
- E_b: Base efficiency (95%)
- P_o: Overtime penalty
- P_r: Rest penalty
- P_p: Patients seen penalty
- W_d: Workload degradation