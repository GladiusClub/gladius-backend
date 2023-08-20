// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GLCToken is ERC20 {
    address private _owner;

    // Event to record transactions
    event TransactionRecord(address indexed from, address indexed to, uint256 amount);

    constructor(uint256 initialSupply) ERC20("GLC Token", "GLC") {
        _mint(msg.sender, initialSupply);
        _owner = msg.sender;
    }

    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    } 

    function mint(address to, uint256 amount) public {
        require(msg.sender == _owner, "Only the contract owner can mint tokens");
        _mint(to, amount);

        // Emit the TransactionRecord event
        emit TransactionRecord(msg.sender, to, amount);
    }

    function transfer(address to, uint256 amount) public override returns (bool) {
        _transfer(msg.sender, to, amount);

        // Emit the TransactionRecord event
        emit TransactionRecord(msg.sender, to, amount);

        return true;
    }
}
