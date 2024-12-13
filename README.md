# Secret Santa Cycle Generator

A command-line tool to create a **Secret Santa cycle** that:

- Ensures no self-gifting.
- Avoids reciprocal gifting.
- Respects partnership constraints (e.g., couples cannot give to each other).

This tool is inspired by the  two-set approach to resolving partnership constraints by [Pista Godo](https://www.linkedin.com/in/pistagodo/). It is designed to handle small to large groups efficiently while maintaining all constraints.

---

## Features

1. **Input Deduplication**:
   - Warns and removes duplicate participants or partnerships before processing.

2. **Validation**:
   - Ensures the number of participants is greater than 2.
   - Limits partnerships to `floor(participants / 2)`.
   - Verifies that all partners exist in the participant list.

3. **Constraint Handling**:
   - Generates a single directed cycle avoiding self-gifting, reciprocal gifting, and partner gifting.

4. **Scalability**:
   - Handles groups of any size, including large groups with hundreds of participants.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/cyberscribe/secret-santa.git
```

### Dependencies

- Python 3+

---

## Usage

### Command-Line Interface

The tool requires two input files:

1. **Participants File**:
   - A text file with one participant per line.

2. **Partners File** (optional):
   - A text file where each line contains a pair of partners, separated by a comma.

### Example

```bash
python3 secret_santa.py --participants participants.txt --partners partners.txt
```

### Output

The tool generates a directed cycle:

```
Participant1 -> Participant2
Participant2 -> Participant3
...
ParticipantN -> Participant1
```

---

## Input File Format

### Participants File

```
Alice
Bob
Charlie
Dave
```

### Partners File

```
Alice,Bob
Charlie,Dave
```

---

## Edge Cases Handled

1. **Minimum Participants**:
   - Ensures more than 2 participants.

2. **Duplicates**:
   - Warns and removes duplicate participants or partnerships.

3. **Highly Constrained Groups**:
   - Handles scenarios where partnerships significantly limit valid cycles.

---

## Development

### Running Tests

You can test the tool with various edge cases by preparing input files and running:

```bash
python3 secret_santa.py --participants test_participants.txt --partners test_partners.txt
```

### Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

---

## Special Thanks**: 

[Pista Godo](https://www.linkedin.com/in/pistagodo/) for the two-set strategy to handle partnership constraints.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

