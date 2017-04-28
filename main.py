import pandas
import datetime
import numpy

xl = pandas.ExcelFile("HouseHoldElectricity.xlsx")

data_frame = xl.parse(xl.sheet_names[0], skiprows=3)


def calculate_power(current_power, percentage_decrease):
    """
    calculates the new power.
    """
    required_power = current_power - (current_power * percentage_decrease)/100.
    return int(required_power)


def make_round(x, base=5):
    """
    Rounds the time in interval of 5 min.
    """
    return int(base * round(float(x)/base))


def get_index(current_time):
    """
    Return index of the current timing.
    """
    current_hour = current_time.hour
    current_minute = make_round(current_time.minute)
    if current_minute == 60:
        current_minute = 00
    current_second = 00
    idx = numpy.where(data_frame['Time'].values == datetime.time(current_hour,
                                                                 current_minute,
                                                                 current_second))
    #idx = numpy.where(data_frame['Time'].values == datetime.time(07, 05, current_second))
    print "Rounded Time to 5 minutes, current time = ", datetime.time(current_hour,
                                                                      current_minute,
                                                                      current_second)
    return idx[0][0]


def subset_sum(numbers, target, min_power, partial=[]):
    """
    Displays the values and names of devices.
    Requested power is target.
    """
    s = sum(partial)
    # check if the partial sum is equals to target

    display_vals = {
        161: "FAN/AC",
        184: "Refrigerator/Microwave",
        230: "gyeser",
        207: "TV"
    }

    print "target", target

    if min_power < 300:
        if s <= target:
            print "%s = %s < %s" % (partial, sum(partial), target)
    else:
        if s <= target and s >= min_power:
            print "%s = %s < %s" % (partial, sum(partial), target)
            for p in partial:
                if p in display_vals.keys():
                    print display_vals[p], p
            print
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, min_power, partial + [n])


def main(percentage_decrease):
    """
    params:
        pdp: power decrease percentage.
        time: time at which they want to reduce the power.
    """
    current_time = datetime.datetime.now().time()
    idx = get_index(current_time)

    device_list = []

    device = {
        "gyeser": {
            "power": 230,
            "active": data_frame['Gyeser'].values[idx]
        },
        "Refrigerator": {
            "power": 184,
            "active": data_frame['Refrigerator'].values[idx]
        },
        "Microwave": {
            "power": 184,
            "active": data_frame['Microwave'].values[idx]
        },
        "FAN": {
            "power": 161,
            "active": data_frame['FAN'].values[idx]
        },
        "AC": {
            "power": 161,
            "active": data_frame['AC'].values[idx]
        },
        "TV": {
            "power": 207,
            "active": data_frame['TV'].values[idx]
        }
    }

    for key, value in device.items():
        for i in range(value['active']):
            device_list.append(value['power'])

    current_power = data_frame['Power'].values[idx]
    required_power = calculate_power(current_power, percentage_decrease)
    min_power = calculate_power(required_power, percentage_decrease*2)

    print "Current Time = ", current_time
    print "Current Power = ", current_power
    print "Requested Power = ", required_power
    print "Sum of Devices should have power of at least ", min_power
    print subset_sum(device_list, required_power, min_power)


if __name__ == "__main__":
    import sys
    percentage_decrease = int(sys.argv[1])
    if percentage_decrease:
        main(percentage_decrease)
    else:
        main(10) # Default value
