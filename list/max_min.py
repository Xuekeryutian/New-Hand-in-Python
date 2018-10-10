def max_min(list):
	count=len(list)
	for i in range(0,count):
		for j in range(eachone+1,count):
			if list[i]<list[j]:
				list[i],list[j]=list[j],list[i]
	print("max_min:",list)
		