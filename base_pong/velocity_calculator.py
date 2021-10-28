class VelocityCalculator:
    # As in the time it took for there to be one iteration  
    time = 0
    def give_velocity(unit_of_measurement, how_many_units):
        """Units are in 1/1000 of the screen 
            screen_length and screen_height are encouraged to be used"""
        return (unit_of_measurement / 1000) * how_many_units

    def calc_distance(velocity):
        return VelocityCalculator.time * velocity
    
    def give_velocity2(acceleration, time, distance):
        return (distance / time) - (acceleration * time / 2)
    # Velocities are in smaller measurements just because they happen alot, but this has 
    # Bigger measurements since its used for widths and stuff like that
    def give_measurement(unit_of_measurement, how_many_units):
        """Units are in 1/100 of the screen 
            screen_length and screen_height are encouraged to be used"""
        return (unit_of_measurement / 100) * how_many_units
    def give_acceleration(distance, time):
        return distance/time ** 2