def halfmean(a,i,j): # Function to take arbitrary mean on a list
	sum=0
	if i<j:
		for k in range (i,j):
			sum+= a[k]
		return sum/(j-i)
	else :
		print('wrong indices')
	

def compare(a): # Function for comparing whether an array is decreasing or increasing
	if halfmean(a,0,int(len(a)/2))<halfmean(a,int(len(a)/2),len(a)):
		print('increasing')
	elif halfmean(a,0,int(len(a)/2))>halfmean(a,int(len(a)/2),len(a)):
		print('decreasing')
	else :
		print ('both sums are equal')

a=[int(i) for i in input('input array: \n').split()]
#print (a) 


compare(a)