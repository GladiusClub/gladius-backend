// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // Enum to represent the NFT types
    enum NFTType {SHIBA_INU, ST_BERNARD, PUG}

    // Mapping to store the CID values of the NFT types
    mapping(NFTType => string) public nftTypeToCID;

    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;

        // Set the CID values for the NFT types
        nftTypeToCID[NFTType.SHIBA_INU] = "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json";
        nftTypeToCID[NFTType.ST_BERNARD] = "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json";
        nftTypeToCID[NFTType.PUG] = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json";
    }

    // This function is called with NFTType enum value to select the NFT type (0: SHIBA_INU, 1: ST_BERNARD, 2: PUG)
    // The `to` address then receives ownership of the newly minted token
    function createCollectible(NFTType nftType, address to) public returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(to, newTokenId);
        string memory tokenURI = nftTypeToCID[nftType];
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
