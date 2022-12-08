pragma solidity >= 0.7.0;

contract Counter {
    int private count = 0;

    function push(int delta) public {
        count += delta;
    }

    function pull(int delta) public {
        if (count > delta) {
            count -= delta;
	}
    }
}
