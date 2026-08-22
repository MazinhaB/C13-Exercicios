% Gráficos 3D

[x,y] = meshgrid(1:0.5:10, 1:20);
z = sin(x) + cos(y);

figure

surf(x, y, z)

colormap("spring")
shading interp

xlabel('x')
ylabel('y')
zlabel('z')

figure
contour(x, y, z)
xlabel('x')
ylabel('y')
zlabel('z')
