main: 
	$a0 = 5;
	$ra = 0; #level 0
	goto fact;
ret0:
	print($v0);
	exit;
	fact:
	if ($a0>1) goto sino;
	$v0 = 1;
	if ($ra==0) goto ret0;
	$ra = $ra - 1;
	goto ret1;
sino:
	$a0 = $a0 - 1;
	$ra = $ra + 1; #level ++
	goto fact;
ret1:
	$a0 = $a0 + 1;
	$v0 = $a0 * $v0;
	if ($ra==0) goto ret0;
	$ra = $ra - 1;
	goto ret1;