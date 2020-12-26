#!/bin/bash
merchant_code=$1
action=$2
time_info=$3

function start(){
	conf_file="/etc/nginx/conf.d/$1"
	if [ ! -f $conf_file ];then
		echo "No such file $1"
		echo "Failure"
	else
		sed -i "/root/s/\/.*;/\/root\/maintain;/g" $conf_file
		sed -i "/if/s/if/#if/g" $conf_file
		sed -i "/time/s/>.*</>$2</g" /root/maintain/index.html
	fi
	return 0
}

function stop(){
	conf_file="/etc/nginx/conf.d/$1"
	if [ ! -f $conf_file ];then
		echo "No such file $1"
		echo "Failure"
	else
		code=`echo $1 | awk -F '.' {'print $1'}`
		sed -i "s/\/root\/maintain/\/root\/$code\/public/g" $conf_file
		sed -i "/if/s/#if/if/g" $conf_file
	fi
	return 0
}

function run(){
	if [ $1 == 'all' ];then
		file_list=`ls -lh /etc/nginx/conf.d/ | grep '^-' | awk {'print $9'}`
		if [ $2 == 'start' ];then
			for file in $file_list
			do
				start $file $3
			done
		elif [ $2 == 'stop' ];then
			for file in $file_list
			do
				stop $file
			done
		else
			echo "Action input error!"
		fi
	else
		if [ $2 == 'start' ];then
			start "$1.conf" $3
		elif [ $2 == 'stop' ];then
			stop "$1.conf"
		else
			echo "Action input error!"
		fi
	fi
	/usr/sbin/nginx -t >/dev/null 2>/dev/null
	if [ $? == 0 ];then
		/usr/sbin/nginx -s reload
		echo "Successful"
	else
		echo "Nginx reload error!"
	fi
}


run $merchant_code $action $time_info