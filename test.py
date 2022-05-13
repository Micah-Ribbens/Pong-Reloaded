#
# if collision_time1 != -1 and collision_time1 < collision_time2:
#     new_ball_x_coordinate, new_ball_y_coordinate = portal_opening2_path._get_coordinates(collision_time1 + portal_opening2_path.total_time)
#     ball_collision_x_coordinate = portal_opening1_path._get_coordinates(collision_time1 + portal_opening1_path.total_time)[0]
#     self._set_portal_path_times(collision_time1, portal_paths)
#
#     total_time += collision_time1
#
# if collision_time2 != -1 and collision_time2 <= collision_time1:
#
#     # Have to add the total times because the collision time is not the time of the velocity path at that
#     # moment it is the time of collision + the current elapsed time for the velocity path
#     new_ball_x_coordinate, new_ball_y_coordinate = portal_opening1_path._get_coordinates(collision_time2 + portal_opening1_path.total_time)
#     ball_collision_x_coordinate = portal_opening2_path._get_coordinates(collision_time2 + portal_opening2_path.total_time)[0]
#     self._set_portal_path_times(collision_time2, portal_paths)
#
#     total_time += collision_time2
#
# if collision_time2 != -1 or collision_time1 != -1:

c = 99
b = 88
k = c + b