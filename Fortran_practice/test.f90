program Calculate_Circle

  implicit none

  real :: diameter, radius, area
  real, parameter :: pi = 3.14

  PRINT *, "Enter:"
  READ *, diameter

  radius = diameter / 2
  area = pi * radius ** 2

  PRINT *, "Radius=", radius, "cm"
  PRINT *, "Area=", area, "cm2"

end program Calculate_Circle
