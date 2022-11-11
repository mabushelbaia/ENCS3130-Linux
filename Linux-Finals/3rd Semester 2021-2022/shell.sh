#!/bin/sh
echo "Enter file name: "
read file
if [ ! -e "$file" ]; then # Checking if file is accessible 
	echo "File doesn't exist"
	exit 
fi
max=0
maxword=""
line=0
for word in `cat $file`; do 
 	n=$(echo "$word" | grep -o -i '[aioue]' | wc -l)
	if [ "$n" -gt "$max" ]; then
		max=$n
		maxword=$word
		line=$(grep -n "$word" $file | cut -d: -f1)
	fi
done
echo "The word with maximum vowels is \"$maxword\" on line $line with $max vowels."
echo "do you want to enter another file? (y/n)"
read choice
if [ "$choice" = "y" ]; then
	./shell.sh
fi
  
