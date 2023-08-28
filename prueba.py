import cv2

# Initialize variables
start_point = None
end_point = None
measuring = False
measurements = []
measurement_id = 1

# Mouse callback function
def measure_distance(event, x, y, flags, param):
    global start_point, end_point, measuring

    if event == cv2.EVENT_LBUTTONDOWN:
        if not measuring:
            start_point = (x, y)
            measuring = True
        else:
            end_point = (x, y)
            measuring = False

# Create a window and set mouse callback
cv2.namedWindow("Distance Measurement")
cv2.setMouseCallback("Distance Measurement", measure_distance)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if start_point is not None:
        cv2.circle(frame, start_point, 5, (0, 0, 255), -1)
    if end_point is not None:
        cv2.circle(frame, end_point, 5, (0, 0, 255), -1)
    if start_point is not None and end_point is not None:
        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
        distance = ((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5
        cv2.putText(frame, f"Distance: {distance:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Distance Measurement", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('m'):
        if start_point is not None and end_point is not None:
            measurements.append({
                'id': measurement_id,
                'start_point': start_point,
                'end_point': end_point,
                'distance': distance
            })
            print(f"Measurement {measurement_id} saved: {start_point} to {end_point}, Distance: {distance:.2f}")
            measurement_id += 1
        start_point = None
        end_point = None

cap.release()
cv2.destroyAllWindows()

# Save measurements to a text file
with open("measurements.txt", "w") as f:
    for measurement in measurements:
        f.write(f"Measurement {measurement['id']}:\n")
        f.write(f"Start Point: {measurement['start_point']}\n")
        f.write(f"End Point: {measurement['end_point']}\n")
        f.write(f"Distance: {measurement['distance']:.2f}\n\n")
