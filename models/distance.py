import math


def dist(lat1,lon1,lat2,lon2):
	r_earth = 6371000 # meters
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	deltaphi = phi2 - phi1
	deltalambda = math.radians(lon2 - lon1)
	a = math.pow(math.sin(deltaphi/2),2) + math.cos(phi1)*math.cos(phi2)*math.pow(math.sin(deltalambda/2),2)
	return r_earth * 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
#test code
#print dist(34,-118,42,-71)

def time(dist):
	#if dist < 1400000:
	#	return 2
	return int(round(dist/700000,0))
#test code
#print time(dist(34,-118,42,-71))
#print time(dist(50,100,-50,-80))
#print time(dist(34,34,34,35))

