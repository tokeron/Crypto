pragma solidity >=0.7.0 <0.9.0;

contract SimpleMultiSigWallet {

    mapping(address => bool) public owners; // List of owners
    uint256 public threshold; // Minimum number of required signatures

    constructor(address[] memory _owners, uint256 _threshold) {
        owners[_owners[0]] = true; // Add first owner for initialization
        threshold = _threshold;
    }

    function addOwner(address newOwner) public onlyOwner {
        owners[newOwner] = true;
    }

    function removeOwner(address owner) public onlyOwner {
        owners[owner] = false;
    }

    function setThreshold(uint256 newThreshold) public onlyOwner {
        threshold = newThreshold;
    }

    modifier onlyOwner() {
        require(owners[msg.sender], "Only owner can call this function");
        _;
    }

    function executeTransaction(address to, uint256 value, bytes memory data) public {
        // Simulate signature verification (simplified)
        uint256 approvalCount = 0;
        for (address owner in owners) {
            if (isSignatureValid(owner, keccak256(abi.encodePacked(to, value, data)))) {
                approvalCount++;
            }
        }
        require(approvalCount >= threshold, "Insufficient signatures");

        // Execute transaction (simplified)
        (bool success, ) = to.call{value: value}(data);
        require(success, "Transaction failed");
    }

    function isSignatureValid(address owner, bytes32 messageHash) public view returns (bool) {
        // Simulate signature verification logic (e.g., ECDSA or pre-approval)
        // Replace with actual signature verification mechanism
        return true;
    }
}
