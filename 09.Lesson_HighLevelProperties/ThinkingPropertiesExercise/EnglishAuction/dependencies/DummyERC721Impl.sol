// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.13;

import "./IERC721Receiver.sol";

/*
    An incomplete implementation of ERC721 that only foscuses on transferFrom and ownership tracking.
    Lacks support for approvals, and some other checks.
*/
contract DummyERC721Impl {
    string public name;
    string public symbol;

    // Mapping from token ID to owner address
    mapping(uint256 => address) private _owners;

    // Mapping owner address to token count
    mapping(address => uint256) private _balances;

    
    function balanceOf(address owner) external view returns (uint256) {
        require(owner != address(0), "ERC721: Zero Address is invalid");
        return _balances[owner];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "ERC721: invalid token ID");
        return owner;
    }

    function _transferFrom(address from, address to, uint256 tokenId) internal {
        require(_owners[tokenId] == from);
        require(to != address(0));
        
        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;
    }

    function transferFrom(address from, address to, uint256 tokenId) external payable {
        _transferFrom(from, to, tokenId);
    }

    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public virtual {
        _transferFrom(from, to, tokenId);
        require(_checkOnERC721Received(from, to, tokenId), "ERC721: transfer to non ERC721Receiver implementer");
    }

    function _checkOnERC721Received(
        address from,
        address to,
        uint256 tokenId
    ) private returns (bool) {
        if (to.code.length > 0) {
            bytes4 retval = IERC721Receiver(to).onERC721Received(msg.sender, from, tokenId, "");
            return retval == IERC721Receiver.onERC721Received.selector;
        } else {
            return true;
        }
    }
}