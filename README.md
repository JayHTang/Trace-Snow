# Trace-Snow

Tracesnow has discontinued their service, which means when you wrap up your tracking session and try to upload, it will always fail.

For Android devices, you can go to /Android/data/com.alpinereplay.android/files/outbox to get the gps file and use this script to parse it into a gpx file.

gpx files are generally accepted by major tracking apps, thus you can import your session into apps like Slopes.

You can download your previous sessions from [traceup](http://snow.traceup.com/settings/gpx)

# usage

```
python tracesnow.py <input gps file path> <output gpx file path>
```
Example:
```
python tracesnow.py data-2021-01-01-10-00-00.gps data-2021-01-01-10-00-00.gpx
```
# Known issues

It took some guess work to understand what the data points means in the gps file. And the meaning of the data in the acc file is still unknown.

Since traceup refuse to provide anything because "all our engineers are currently focused on improving the app for Soccer", no offical documents or guidance can be obtained.

As a result, speed appears to be slower than it should be.
