main:
    $t1 = 0;
    $t2 = 0; 
while:     
    if ($t1>=4) goto end;
    $t2 = $t2 + $t1;     
    $t1 = $t1 + 1;     
    goto while; 
end:     
    print($t2); 