// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.20; 
 
/** 
 * @title SimpleStorage 
 * @dev A basic contract that lets you store and retrieve a number. 
 */ 
contract SimpleStorage { 
 
    uint256 private myNumber; 
 
    /** 
     * @dev Stores a new number. 
     * @param _newNumber The new number to store. 
     */ 
    function store(uint256 _newNumber) public { 
        myNumber = _newNumber; 
    } 
 
    /** 
     * @dev Retrieves the stored number. 
     * @return The currently stored number. 
     */ 
    function retrieve() public view returns (uint256) { 
        return myNumber; 
    } 
} 