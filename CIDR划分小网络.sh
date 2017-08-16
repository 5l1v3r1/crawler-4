
myiplist="10.0.0.0/15" #10.0.0.0-10.0.63.255    (16384)
postfix=23
mynum=`expr 32 - $postfix`  #指数
mytwo=2
myzero=0
classmax=256
msubmask=$(awk 'BEGIN{print '"$mytwo"'^'"$mynum"'}' )  # 256 / 512 内存小则指定24postfix
num=`expr $msubmask / 256`  #如果postfix 是23 则是2， 24则是1

num1=$(echo $myiplist |awk -F "/" '{print$1}') #求 a.b.c.d
classA=$(echo $num1 |awk -F"." '{print$1}')
classB=$(echo $num1 |awk -F"." '{print$2}')
classC=$(echo $num1 |awk -F"." '{print$3}')
classD=$(echo $num1 |awk -F"." '{print$4}')

num2=$(echo $myiplist |awk -F "/" '{print$2}') 

if  [ "$num2" -lt $postfix ] ;   #分割成小网段
then
echo ok
#求总ip数
mynum2=`expr 32 - $num2` #
sumip=$(awk 'BEGIN{print '"$mytwo"'^'"$mynum2"'}' )

#划分ip
mynumC=`expr $sumip / $classmax` 
if  [ "$mynumC" -lt "256" ] ;  #在a.b.c.d 的 c里
then
#在a.b.c.d的c里
classCmax=`expr $mynumC - 1` #64-1 =~ 10.0.63.255
classCmin=$classC

#按照 /postfix 罗列出ip列表
while [ $classCmin -lt `expr $classCmax - 1` ];  ## <= le
##10.0.0.0-10.0.63.255
do
myip="$classA.$classB.$classCmin.$classD/$postfix"
echo $myip
if [ "$classCmin" -gt "256" ] ;  #出错跳出循环
then
break
fi

classCmin=`expr $classCmin + $num` # 按照开头变量需求变更ip
done

else
#在a.b.c.d的b里
echo b
if [ "$mynumC" -gt "256" ] ;  #出错跳出循环
then
break
fi
classBmin=$classB
mynumB=`expr $sumip / $classmax / $classmax - 1`  #b
classBmax=`expr $classBmin + $mynumB`
echo $classBmax
echo "$classA.$classBmax.$classC.$classD/$postfix"

classCmax=`expr $classmax - 1` #256-1
classCmin=$classC

#按照 /postfix 罗列出ip列表 b
while [ $classBmin -lt `expr $classBmax + 1` ];  #
do #b

while [ $classCmin -le `expr $classCmax - 1` ];  
do #c
myip="$classA.$classBmin.$classCmin.$classD/$postfix"
echo $myip
if [ "$classCmin" -ge `expr $classmax + $num + $num ` ] ;  #出错跳出循环
then
break
fi

classCmin=`expr $classCmin + $num` # 按照开头变量需求变更ip
done #c

classBmin=`expr $classBmin + 1` 
classCmin=0
done #b


fi #划分ip

else
echo big
fi #


