import math

def dist(lat1,lon1,lat2,lon2):
	r_earth = 6371000 # meters
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	deltaphi = phi2 - phi1
	deltalambda = math.radians(lon2 - lon1)
	a = math.pow(math.sin(deltaphi/2),2) + math.cos(phi1)*math.cos(phi2)*math.pow(math.sin(deltalambda/2),2)
	return r_earth * 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))

def time(dist):
	return int(round(dist/700000,0))

