function plotSphere(x0, y0, z0, R)
	PREC = 0.1;
	[theta, phi] = meshgrid(0:PREC:2*pi, -pi/2:PREC:pi/2);
	x = x0 + R * cos(theta) .* cos(phi);
	y = y0 + R * sin(theta) .* cos(phi);
	z = z0 + R * sin(phi);
	xp = x ./ z;
	yp = y ./ z;
	figure;
	plot(xp', yp', '-');
	axis('equal');


