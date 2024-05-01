// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@gnosis.pm/safe-contracts@1.3.0/contracts/GnosisSafe.sol";

contract MultisigWallet is GnosisSafe {
    uint public n; // The total number of keys
    mapping(address => bool) public isKeyOwner; // Tracks if an address is an owner
    uint public transactionCount; // Tracks the number of transactions
    uint public required; // The number of required confirmations

    struct Transaction {
        address destination;
        uint value;
        bytes data;
        bool executed;
        uint confirmations;
        uint timestamp;
    }

    mapping(uint => Transaction) public transactions;
    mapping(uint => mapping(address => bool)) public confirmations;
    mapping(uint => uint) public lastConfirmedTime; // Tracks the last confirmation time for delayed transactions

    event SubmitTransaction(
        address indexed owner,
        uint indexed transactionId,
        address indexed destination,
        uint value,
        bytes data
    );
    event ConfirmTransaction(address indexed owner, uint indexed transactionId);
    event RevokeConfirmation(address indexed owner, uint indexed transactionId);
    event ExecuteTransaction(address indexed owner, uint indexed transactionId);

    modifier onlyOwner() {
        require(isKeyOwner[msg.sender], "Not owner");
        _;
    }

    modifier transactionExists(uint _transactionId) {
        require(transactions[_transactionId].destination != address(0), "Transaction does not exist");
        _;
    }

    modifier notExecuted(uint _transactionId) {
        require(!transactions[_transactionId].executed, "Transaction already executed");
        _;
    }

    modifier notConfirmed(uint _transactionId) {
        require(!confirmations[_transactionId][msg.sender], "Transaction already confirmed");
        _;
    }

    function setupOwners_(address[] memory _owners, uint _required) public {
        require(n == 0, "Owners already set");
        require(_owners.length > 0, "Owners required");
        require(_required > 0 && _required <= _owners.length, "Invalid required number of owners");

        for (uint i = 0; i < _owners.length; i++) {
            address owner = _owners[i];
            require(owner != address(0), "Invalid owner");
            require(!isKeyOwner[owner], "Owner not unique");

            isKeyOwner[owner] = true;
        }

        n = _owners.length;
        required = _required;
    }

    function submitTransaction(
        address _destination,
        uint _value,
        bytes memory _data,
        address[] memory _keys
    ) public onlyOwner {
        require(_keys.length > 0 && _keys.length <= n, "Invalid number of keys");

        // Verify each key
        for (uint i = 0; i < _keys.length; i++) {
            require(isKeyOwner[_keys[i]], "Invalid key");
        }

         // Check if there's an existing transaction that can be replaced
        uint existingTransactionId = findExistingTransaction(_destination, _value, _data);
        if (existingTransactionId != type(uint).max && transactions[existingTransactionId].confirmations < _keys.length) {
            // Replace the existing transaction with the new one
            uint transactionId = replaceTransaction(existingTransactionId, _destination, _value, _data, _keys);
        } else {
            // No existing transaction to replace, create a new one
            uint transactionId = transactionCount;
            transactions[transactionId] = Transaction({
            destination: _destination,
            value: _value,
            data: _data,
            executed: false,
            confirmations: 0,
            timestamp: block.timestamp
        });
        transactionCount += 1;

        // Confirm the transaction with each key
        for (uint i = 0; i < _keys.length; i++) {
            confirmTransaction(transactionId, _keys[i]);
        }

        if (_keys.length < n) {
            lastConfirmedTime[transactionId] = block.timestamp + 24 hours;
        }
        emit SubmitTransaction(msg.sender, transactionId, _destination, _value, _data);
        }
    }

    // Modified confirmTransaction function to include key parameter
    function confirmTransaction(uint _transactionId, address _key) public onlyOwner transactionExists(_transactionId) notExecuted(_transactionId) notConfirmed(_transactionId) {
        require(isKeyOwner[_key], "Invalid key");
        confirmations[_transactionId][_key] = true;
        transactions[_transactionId].confirmations += 1;
        emit ConfirmTransaction(_key, _transactionId);
        if (transactions[_transactionId].confirmations == n || block.timestamp >= lastConfirmedTime[_transactionId]) {
            executeTransaction(_transactionId);
        }
    }


    function executeTransaction(uint _transactionId) public onlyOwner transactionExists(_transactionId) notExecuted(_transactionId) {
        require(transactions[_transactionId].confirmations >= required, "Not enough confirmations");
        if (transactions[_transactionId].confirmations < n && block.timestamp < lastConfirmedTime[_transactionId]) {
            revert("Transaction delayed due to security");
        }
        transactions[_transactionId].executed = true;
        (bool success, ) = transactions[_transactionId].destination.call{value: transactions[_transactionId].value}(transactions[_transactionId].data);
        require(success, "Transaction failed");
        emit ExecuteTransaction(msg.sender, _transactionId);
    }

    function replaceTransaction(uint _transactionId, address _newDestination, uint _newValue, bytes memory _newData, address[] memory _keys) 
    public onlyOwner transactionExists(_transactionId) notExecuted(_transactionId)  returns (uint newTransactionId) {
        require(transactions[_transactionId].confirmations > required, "Not enough confirmations for replacement");
        require(isKeyOwner[msg.sender], "Only an owner can replace a transaction");

        // Cancel the existing transaction
        transactions[_transactionId].executed = true;

        // Submit the new transaction
        uint newTransactionId = transactionCount;
        transactions[newTransactionId] = Transaction({
            destination: _newDestination,
            value: _newValue,
            data: _newData,
            executed: false,
            confirmations: 0,
            timestamp: block.timestamp
        });
        transactionCount += 1;

        emit SubmitTransaction(msg.sender, newTransactionId, _newDestination, _newValue, _newData);
        return newTransactionId;
    }

    // Helper function to find an existing transaction with the same details
    function findExistingTransaction(address _destination, uint _value, bytes memory _data) internal view returns (uint) {
        for (uint i = 0; i < transactionCount; i++) {
            if (transactions[i].destination == _destination &&
                transactions[i].value == _value &&
                keccak256(transactions[i].data) == keccak256(_data) &&
                !transactions[i].executed) {
                return i;
            }
        }
        return type(uint).max; // Return max uint value if no existing transaction is found
}
}