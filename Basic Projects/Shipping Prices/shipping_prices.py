# Variables
weight = 28

# Ground Shipping
cost_ground = ""
if weight <= 2:
  cost_ground = weight * 1.5 + 20
elif 2 < weight <= 6:
  cost_ground = weight * 3 + 20
elif 6 < weight <= 10:
  cost_ground = weight * 4 + 20
elif weight > 10:
  cost_ground = weight * 4.75 + 20

cost_ground_premium = 125

# Drone Shipping
cost_drone = ""
if weight <= 2:
  cost_drone = weight * 4.50
elif 2 < weight <= 6:
  cost_drone = weight * 9
elif 6 < weight <= 10:
  cost_drone = weight * 12
elif weight > 10:
  cost_drone = weight * 14.25

# Output
print("Ground Shippping $", cost_ground)
print("Ground Shipping Premium $", cost_ground_premium)
print("Drone Shipping: $", cost_drone)
