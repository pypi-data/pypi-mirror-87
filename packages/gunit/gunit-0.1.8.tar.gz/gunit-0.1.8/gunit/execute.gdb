b gunit_hook
b gunit_end

commands 1
 silent
 !date +%s.%N >> $GUNIT_GDBTIMES
 printf "TESTx\n"
 printf "FILE %s\n", file
 printf "LINE %d\n", line_number
 printf "PASS %d\n", (result == expected) ^ no
 printf "EXPECT %d\n", expected
 printf "RESULT %d\n", result
 printf "BACKTRACE\n"
 bt
 !date +%s.%N >> $GUNIT_GDBTIMES
 c
end

commands 2
 silent
 set logging off
 quit
end

!date +%s.%N > $GUNIT_GDBTIMES

c
run
