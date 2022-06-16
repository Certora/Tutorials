
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

rule neverReachPlayer4AsRule(method f){
    env e; calldataarg args;

    uint256 _position = ballAt();
    require _position != 3 && _position != 4;

    f(e, args);

    uint256 position_ = ballAt();
    assert position_ != 3 && position_ != 4, "The ball is at the hands of player 4 or 3";
}