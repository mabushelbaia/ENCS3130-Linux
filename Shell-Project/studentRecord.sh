#!/bin/sh

echo "Enter file name: "
read file
if [ ! -e "$file" ]; then # Checking if file is accessible 
	echo "File doesn't exist"
	exit 
fi


Cal_Semester() {  # Function to show the average or passed hours of a semester mode = '1' : Average , mode = '2': Hours
	k=1
	line=$(sed -n "$k"p $file)
	until [  -z "$line" ]; do
		temp_Hours=0
		temp_score=0
		courses=" "
		j=1
		semester=$(echo "$line" | cut -d';' -f1) # semester name
		line=$(echo $line | cut -d';' -f2)  # semester courses
		until [ -z "$courses" ]; do
			courses=$(echo "$line" | cut -d',' -f$j)  #  course by course
			grade=$(echo "$courses" | cut -d' ' -f3) 
			assignedHours=$(echo "$courses" | cut -d' ' -f2 | tr -d -c 0-9 | cut -c2)
			if [ "$grade" = "F" ]; then 
				grade=50
			elif [ "$grade" = "FA" ]; then
				grade=55
			elif [ "$grade" = "I" ]; then
				j=$((j+1))
				continue
			fi
			temp_score=$((temp_score+ grade*assignedHours))
			temp_Hours=$((temp_Hours+assignedHours))
			j=$((j+1))
		done
		if [ "$1" = "1" ]; then
			printf "$semester: %.2f%%\\n" "$((100 *   temp_score/temp_Hours ))e-2"
		elif [ $1 = "2" ]; then
			echo "$semester: $((temp_Hours))"
		fi
		k=$((k+1))
		line=$(sed -n "$k"p $file) # next line
	done
}

addSemester() { # as name suggests
	echo "Enter Data using format YEAR/SEMESTER; Course1 Grade1, Course2 Grade2, ..."
	read input
	semester=$( echo "$input" | cut -d';' -f1 ) # getting semester name
	if grep "^\<$semester\>;" $file > /dev/null; then echo "Semester already exists!"; return; fi # checking if semester already exists
	if  [ `echo $semester | cut -c11` -gt 3 -o `echo $semester | cut -c11` -lt 1 ]; then echo "Invalid format"; return; fi # checking if input is vaild
	if  [ ! $((`echo $semester | cut -c9` - `echo $semester | cut -c4`))  -eq 1 ]; then echo "Invalid format"; return; fi # checking if input is vaild
	if  ! echo "$input" | grep ',' > /dev/null ; then echo "Invalid Input";return; fi # checking if input is vaild
	if  ! echo "$input" | grep ';' > /dev/null ; then echo "Invalid Input";return; fi # checking if input is vaild
	courses=$(echo $input | cut -d';' -f2 ) # getting courses list
	p=1
	course=$(echo "$courses" | cut -d',' -f"$p") # course by course
	totalHours=0
	until [ -z "$course" ]; do
		courseCode=$(echo "$course" | cut -d' ' -f2 | tr -d -c 0-9 ) # split the course code into code only ENEE2304 -> 2304
		courseName=$(echo "$course" | cut -d' ' -f2 | tr -d -c A-Z ) # split the course code into name only ENEE2304 -> ENEE
		if [ "$courseCode" -lt 2000 -o "$courseCode" -gt 5999 ]; then echo "Invalid Code!"; return; fi # checking if code is in range
		if [ ! $courseName = "ENEE" ] && [ ! $courseName = "ENCS" ]; then echo "Invalid Code!"; return; fi # checking if name is in range
		totalHours=$((totalHours + `echo "$courseCode" | cut -c2`)) 
		courseGrade=$(echo "$course" | cut -d' ' -f3)
		if [ "$courseGrade" = "F" -o "$courseGrade" = "FA" -o "$courseGrade" = "I" ]; then p=$((p+1));
		elif [ "$courseGrade" -ge 60 -o "$courseGrade" -le 99 ]; then p=$((p+1));
		else echo "Invalid Grade!"; return;
		fi
		course=$(echo "$courses" | cut -d',' -f"$p")
	done
	if [ $totalHours -lt 12 ]; then echo "Hours Less than 12"; return; fi # checking if hours are greater than 12
	echo "$input" >> $file
}

changeGrade() { # as name suggests
	echo "Enter course: "
	read c_name
	if ! grep "$c_name" $file > /dev/null; then echo "Course not found"; return; fi
	echo "Enter Grade: "
	read c_grade
	if [  "$c_grade" -ge 60 -a "$c_grade" -le 99 ]; then :;
	elif [ "$c_grade" = "F" -o "$c_grade" = "FA" ]; then :;
	else echo "Invalid Grade"; return; fi
	old_grade=$(tac $file |  grep -m1 -o "$c_name .\{1,2\}," | grep -o '\<.\{1,2\}\>') # greping the last occurance of a given course
	echo "Old Grade: $old_grade , New Grade: $c_grade, Confirm? (Y or N)"
	read in
	if [ "$in" = "Y" -o "$in" = "y" ]; then
		tac $file | sed "0,/"$c_name" .\{1,2\},/s//"$c_name" "$c_grade",/" > /tmp/$$  # changing the grade of the last occurance
		tac /tmp/$$ > $file  # redirecting the file into our file
	else 
		return
	fi
}


# method to create a file containg all taken courses [ Unique ]
i=1
line=$(sed -n "$i"p $file)
if [ -e data ]; then rm data; fi # if file exists delete it
touch ./data # create a new file
until [  -z "$line" ]; do
	courses=" "
	j=1
	line=$(echo $line | cut -d';' -f2) 
	until [ -z "$courses" ]; do
		courses=$(echo "$line" | cut -d',' -f$j)
		if [ -z "$courses" ]; then continue; fi
		courseCode=$(echo "$courses" | cut -d' ' -f2)
		courseGrade=$(echo "$courses" | cut -d' ' -f3)
		if [ "$courseGrade" = "I" ]; then
			j=$((j+1))
			continue
		fi
		if grep "$courseCode" data > /dev/null; then # if course exists and grade != I delete the course and add the new read one
			sed -i "/$courseCode/d" ./data
		fi
		echo $courses >> data
		j=$((j+1))
	done
	i=$((i+1))
	line=$(sed -n "$i"p $file) # next line
done
## calculating average from the data file we created
i=1
Summation=0
PassedHours=0
FailedHours=0
Lectures=0
Labs=0
temp=$(sed -n "$i"p ./data)
until [ -z "$temp" ]; do
	grade=$(echo "$temp" | cut -d' ' -f2)
	name=$(echo "$temp" | cut -d' ' -f1)
	assignedHours=$(echo "$name" | tr -d -c 0-9 | cut -c2)
	if [ "$assignedHours" -eq 1 ]; then Labs=$((Labs+1)); else Lectures=$((Lectures+1)); fi
	if [ "$grade" = "F" ]; then Summation=$((Summation + assignedHours*55)); FailedHours=$((FailedHours+assignedHours))
	elif [ "$grade" = "FA" ]; then Summation=$((Summation + assignedHours*50)); FailedHours=$((FailedHours+assignedHours))
	else Summation=$((Summation + assignedHours*grade)); PassedHours=$((PassedHours+assignedHours))
	fi
	i=$((i+1))
	temp=$(sed -n "$i"p ./data)
done

ShowSemster () { 
	echo "\n=========="
	echo "Enter Semseter: (Use Y1-Y2:S) "
	read semester
	echo "\n"
	line=$(grep "^\<$semester\>;" $file) #shows the semester
	if [ -z "$line" ]; then
		echo "Semseter not Found"
		exit
	fi
	echo $line
	echo "==========\n"
}


echo "
1.Show or print student records (all semesters).
2.Show or print student records for a specific semester.
3.Show or print the overall average.
4.Show or print the average for every semester.
5.Show or print the total number of passed hours.
6.Show or print the percentage of total passed hours in relation to total F and FA hours.
7.Show or print the total number of hours taken for every semester.
8.Show or print the total number of courses taken.
9.Show or print the total number of labs taken.
10.Insert the new semester record.
11.Change in course grade.
0.Quit"


read option #case to show options
case $option in
	1) echo "==========\n$(cat $file)\n==========";;
	2) ShowSemster;;
	3) 
echo "=========="
printf "Average: %.2f%%\\n" "$((100 *   Summation/(PassedHours+FailedHours) ))e-2"
echo "==========";;
	4) echo "==========\n$(Cal_Semester "1")\n==========";;
	5) echo "==========\nPassedHours: $((PassedHours))\n==========";;
	6)
echo "=========="
printf "Passed: %.2f%%\\n" "$((100 *   PassedHours/(PassedHours+FailedHours) ))e-2"
printf "Failed: %.2f%%\\n" "$((100 *   FailedHours/(PassedHours+FailedHours) ))e-2"
echo "==========";;
	7) echo "==========\n$(Cal_Semester "2")\n==========";;
	8) echo "==========\nCourses: $((Labs+Lectures))\n==========";;
	9) echo "==========\nLabs: $((Labs))\n==========";;
	10) addSemester;;
	11) changeGrade;;
	* ) echo "Illegal Input";;
esac
