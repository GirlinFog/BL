// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Storage {
    uint256 public myNumber;

    function store(uint256 _num) public {
        myNumber = _num;
    }

    function retrieve() public view returns (uint256) {
        return myNumber;
    }
}
