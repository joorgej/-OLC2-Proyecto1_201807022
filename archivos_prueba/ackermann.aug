main:
    $s0 = array(); # stack
    $sp = -1; # null pointer
    $a0 = 3; # m
    $a1 = 9; # n
    $sp = $sp + 1;
    $s0[$sp] = $a0; # push
    goto ack;

ret0:
    print($v0);
    exit;

ack:
    if ($sp < 0) goto ret3; # empty stack
    $a0 = $s0[$sp]; # pop
    $sp = $sp - 1;
    if ($a0 != 0) goto ret1;
    $t4 = $a0 + 1;
    $a1 = $a1 + $t4;
    goto ack;

ret1:
    if ($a1 != 0) goto ret2;
    $a1 = $a1 + 1;
    $a0 = $a0 - 1; # --m
    $sp = $sp + 1;
    $s0[$sp] = $a0; # push
    goto ack;

ret2:
    $a0 = $a0 - 1; # --m
    $sp = $sp + 1;
    $s0[$sp] = $a0;
    $a0 = $a0 + 1; # ++m
    $sp = $sp + 1;
    $s0[$sp] = $a0; # push
    $a1 = $a1 - 1;
    goto ack;

ret3:
    $v0 = $a1;
    goto ret0;