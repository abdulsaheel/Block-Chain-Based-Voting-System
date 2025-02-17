
# Blockchain Based Voting System

A basic blockchain-based voting system to demonstrate how blockchain technology can be used to create a secure and tamper-proof voting mechanism.

## Overview

This project implements a voting system using blockchain technology. The system allows users to vote for one of three political parties: BRS, CONGRESS, or CPI. Each vote is recorded in the blockchain with the voter's hashed details for security and immutability. The system also provides endpoints to view the number of votes each party has received, cast votes, and validate the blockchain's integrity.

## Features

- **Blockchain Integration**: Secure and immutable record of votes.
- **Simple Proof-of-Work**: Mining mechanism to add blocks to the blockchain.
- **Vote Casting**: Allows users to vote for a party.
- **Vote Counting**: Displays the number of votes each party has received.
- **Blockchain Validation**: Ensures the integrity of the blockchain.

## Technologies Used

- **Flask**: Web framework for building the API.
- **Flask-SQLAlchemy**: ORM for managing the SQLite database.
- **SQLite**: Lightweight database for persisting blockchain data.
- **Hashlib**: For creating secure hashes of voter's details.
- **JSON**: For handling transactions.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/blockchain-voting-system.git
   ```
   
2. Navigate to the project directory:
   ```sh
   cd blockchain-voting-system
   ```

3. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```sh
   pip install Flask Flask-SQLAlchemy
   ```

## Running the Application

1. Run the Flask application:
   ```sh
   python voting_system.py
   ```

2. The application will be available at `http://127.0.0.1:5000/`.

## API Endpoints

- **Get Votes**
  - **Endpoint**: `GET /get_votes`
  - **Description**: Returns the number of votes for each party.
  - **Response**:
    ```json
    {
      "parties": {
        "BRS": 10,
        "CONGRESS": 5,
        "CPI": 3
      }
    }
    ```

- **Cast Vote**
  - **Endpoint**: `POST /cast_vote`
  - **Request Body**:
    ```json
    {
      "name": "John Doe",
      "party": "BRS"
    }
    ```
  - **Description**: Allows a user to cast a vote. The voter's name is hashed and linked to the party they vote for.
  - **Response**:
    ```json
    {
      "message": "Vote casted for BRS. Your ID is <hashed_id>.",
      "block_index": 2
    }
    ```

- **Check Blockchain Validity**
  - **Endpoint**: `GET /is_valid`
  - **Description**: Checks if the blockchain is valid.
  - **Response**:
    ```json
    {
      "message": "The blockchain is valid."
    }
    ```

## Example Usage

1. **Get current vote counts**:
   ```sh
   curl -X GET http://127.0.0.1:5000/get_votes
   ```

2. **Cast a vote**:
   ```sh
   curl -X POST http://127.0.0.1:5000/cast_vote -H "Content-Type: application/json" -d '{"name": "Alice", "party": "CONGRESS"}'
   ```

3. **Validate the blockchain**:
   ```sh
   curl -X GET http://127.0.0.1:5000/is_valid
   ```

## Contributing

Feel free to fork the repository and submit pull requests. Contributions to enhance functionality or improve code quality are welcome.


## Contributers 
[Abdul Sahil](https://github.com/abdulsaheel)
[Mittapalli Ashiesh](https://github.com/9441ashiesh)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [Abdul Sahil](mailto:abdulsaheel81@gmail.com)

