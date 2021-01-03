import sys
from datetime import datetime
from typing import List
from xml.dom import minidom


class GPS:
    def __init__(self, lat, lon, ele, time, speed, azimuth):
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.time = time
        self.speed = speed
        self.azimuth = azimuth


def trace_reader(filename: str) -> List[GPS]:
    gps_list = []
    with open(filename) as file:
        lines = file.readlines()
        lat, lon, ele, time = 0, 0, 0, 0
        for line in lines[4:]:
            if line.startswith('H'):
                time, lat, lon, ele, _ = map(float, line.split(',')[1:6])
            else:
                time_, lat_, lon_, ele_, speed, azimuth = map(float, line.split(',')[1:])
                gps_list.append(
                    GPS(lat + lat_ / 1000000, lon + lon_ / 1000000, ele + ele_ / 10, time + time_, speed, azimuth)
                )
    return gps_list


def trace_xml_writer(filename: str, gps_list: List[GPS]) -> int:
    count = 0

    # make xml
    root = minidom.Document()
    gpx = root.createElement('gpx')
    gpx.setAttribute('version', '1.1')
    gpx.setAttribute('creator', 'ActiveReplay')
    gpx.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.setAttribute('xmlns:gte', 'http://www.gpstrackeditor.com/xmlschemas/General/1')
    gpx.setAttribute('targetNamespace', 'http://www.topografix.com/GPX/1/1')
    gpx.setAttribute('elementFormDefault', 'qualified')
    gpx.setAttribute('xsi:schemaLocation',
                     'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
    root.appendChild(gpx)

    trk = root.createElement('trk')
    gpx.appendChild(trk)

    trkseg = root.createElement('trkseg')
    trk.appendChild(trkseg)

    for gps in gps_list:
        trkpt = root.createElement('trkpt')
        trkpt.setAttribute('lat', f'{gps.lat:.6f}')
        trkpt.setAttribute('lon', f'{gps.lon:.6f}')
        trkseg.appendChild(trkpt)

        ele = root.createElement('ele')
        ele.appendChild(root.createTextNode(f'{gps.ele:.2f}'))
        trkpt.appendChild(ele)

        time = root.createElement('time')
        time.appendChild(root.createTextNode(
            datetime.utcfromtimestamp(gps.time / 1000).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + 'Z'
        ))
        trkpt.appendChild(time)

        ext = root.createElement('extensions')
        trkpt.appendChild(ext)

        gte = root.createElement('gte:gps')
        gte.setAttribute('speed', f'{gps.speed:.1f}')
        gte.setAttribute('azimuth', f'{gps.azimuth:.1f}')
        ext.appendChild(gte)

        count += 1

    # write xml
    with open(filename, 'w') as file:
        file.write(root.toprettyxml(indent='\t'))

    return count


def run():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python tracesnow.py <input gps file path> <output gpx file path>")
        print()
        return
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    gps_list = trace_reader(file_in)
    print(f'Successfully wrote {trace_xml_writer(file_out, gps_list)} data points to {file_out}')


if __name__ == '__main__':
    run()
