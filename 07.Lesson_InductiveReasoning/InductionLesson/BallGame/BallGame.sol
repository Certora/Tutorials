
contract BallGame {
	uint256 public ballAt = 3;

	function pass() public {
		require (ballAt >= 1 && ballAt <= 4);
		if (ballAt == 1)
			ballAt = 2;
		else if (ballAt == 2)
			ballAt = 1;
		else if (ballAt == 3)
			ballAt = 4;
		else if (ballAt == 4)
			ballAt = 3;
	}
    
}