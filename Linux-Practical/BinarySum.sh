#!/bin/sh
echo "Enter two 4-bit or less binary numbers: "
read number1
read number2
number1_len=$(($(echo $number1 | wc -c) - 1))
number2_len=$(($(echo $number1 | wc -c) - 1))
if [ $number1_len -lt 0 -o $number1_len -gt 4 -a $number2_len -lt 0 -o $number2_len -gt 4 ]; then 
	echo "invalid input"
else
	check_binary1=$(echo $number1 | tr -d 0-1)
	check_binary2=$(echo $number2 | tr -d 0-1)
	if [ -z "$check_binary1" -a -z "$check_binary2" ]; then
		binary1=$( printf "%4d" $number1 | tr " " "0")
		binary2=$( printf "%4d" $number2 | tr " " "0")
		echo $binary2 $binary1
		output_temp=$(echo ";ibase=2;obase=2;$binary2+$binary1" | bc) 
		output=$( printf "%4d" $output_temp | tr " " "0")
		echo $output
	else 
		echo "invalid - input"
	fi

fi