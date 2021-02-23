echo "Init founder or simple user ? "
read input
if [ $input == "founder" ];
then
	python3 ./py_src/init_founder.py
elif [ $input == "user" ];
then
	python3 ./py_src/init_user.py
else
	echo "Aborted"
fi
