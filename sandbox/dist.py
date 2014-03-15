#!/usr/bin/env python
from geopy import distance
from geopy import Point

# lat, log
p1 = Point("53.4235217000000020 -113.4741271000000040")
p2 = Point("53.5343457999999970 -113.5013688000000229")
result = distance.distance(p1, p2).kilometers
print result

# function() {
#     if (!this.location) {
#         return;
#     }
#
#     this.location.longitude
#
#     forEach(function(tag) {
#         emit(tag, 1);
#     });
# }
#         """)
#
#         reduce_code = Code("""
# function(key, values) {
#     var count = 0;
#
#     for (var i = 0; i < values.length; i++) {
#         count += values[i];
#     }
#
#     return count;
# }
