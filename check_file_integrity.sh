#!/bin/bash

# if [ -n file.txt ]
# then
#  echo "everything is good"
# else
#  mail -s "file.txt size is zero, please fix. " myemail@gmail.com < /dev/null
#  # Grab wget as a fallback
#  wget -c https://www.server.org/file.txt -P /root/tmp --output-document=/root/tmp/file.txt
#  mv -f /root/tmp/file.txt /var/www/file.txt
# fi
#
#
# file=file.txt
# minimumsize=90000
# actualsize=$(wc -c <"$file")
# if [ $actualsize -ge $minimumsize ]; then
#     echo size is over $minimumsize bytes
# else
#     echo size is under $minimumsize bytes
# fi


INPUT=$0
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read flname dob ssn tel status
do
	echo "Name : $flname"
	echo "DOB : $dob"
	echo "SSN : $ssn"
	echo "Telephone : $tel"
	echo "Status : $status"
done < $INPUT
IFS=$OLDIFS

file=
for file in $files
if [ -s $file ]
then
  echo "&file works"
else
  echo "&file needs to be redownloaded"
