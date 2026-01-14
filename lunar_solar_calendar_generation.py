#############################################
# Generate Birthday Calendar
# 生成农历生日日历文件

# Author: EmeraldCherrio
# Website: www.cherrio.xin

# This script generates an iCalendar file (.ics) containing birthday events for the next 100 years for any amount of people you want to add. Import the file into the calendar to subscribe. You can re-run the script and import it into the same calendar to update the birthdays of new people.
# 这个脚本生成了一个.ics的日历文件，包含了未来100年内任意数量的人的生日事件。将该文件导入日历中即可实现订阅。后续重新可重新运行软件并在同一个日历中导入来实现更新新的人的生日。

# This script can realize the conversion between lunar and solar dates, that is, you can input the solar birthday and get the lunar birthday subscription in the .ics file, or vice versa.
# 该脚本实现了农历生日和阳历生日之间的转换，即你可以输入阳历生日并在.ics文件中获得农历生日订阅，反之亦然。

# This code recognizes leap months in lunar birthdays, so an additional input option is added when entering the lunar birthday to determine whether it is a leap month.
# 该代码识别了农历生日中的闰月，因此在输入农历生日时添加了一个额外的输入选项，用于确定是否为闰月。
#############################################

# Required Libraries: ics, lunarcalendar. You can install them using 'pip install ics lunarcalendar'.
# 需要的库：ics, lunarcalendar。你可以使用'pip install ics lunarcalendar'来安装它们。

# If run in Jupyter Notebook, please use the following code to install the required libraries:
# 如果在Jupyter Notebook中运行，请使用以下代码来安装所需的库：
# !pip install ics lunarcalendar

from ics import Calendar, Event
from datetime import datetime
from lunarcalendar import Converter, Solar, Lunar


def add_birthday_event(calendar, name, solar_date, description, years=100):
    """
    Add birthday events to the calendar for the next `years` years based on the given solar date.
    """
    current_year = solar_date.year
    for offset in range(years):
        target_year = current_year + offset
        try:
            event_date = datetime(target_year, solar_date.month, solar_date.day)

            # Add event to the calendar
            event = Event()
            event.name = f"{name}'s {description} Birthday"
            event.begin = event_date
            event.make_all_day()
            calendar.events.add(event)
        except ValueError as e:
            print(f"Skipping year {target_year} due to error: {e}")


def add_birthday_event_lunar(calendar, name, lunar_date, description, is_leap_month=False, years=100):
    """
    Add birthday events based on the input lunar date.
    Generate events for the next `years` years for the given lunar date.
    """
    lunar_month = lunar_date.month
    lunar_day = lunar_date.day
    for year_offset in range(years):
        target_year = lunar_date.year + year_offset
        try:
            # Convert the lunar date to solar date for the target year
            target_lunar_date = Lunar(target_year, lunar_month, lunar_day, is_leap_month)
            target_solar_date = Converter.Lunar2Solar(target_lunar_date)
            event_date = datetime(target_solar_date.year, target_solar_date.month, target_solar_date.day)

            # Add event to the calendar
            event = Event()
            event.name = f"{name}'s {description} Birthday"
            event.begin = event_date
            event.make_all_day()
            calendar.events.add(event)
        except Exception as e:
            print(f"Skipping year {target_year} due to error: {e}")


def main():
    cal = Calendar()

    while True:
        print("\nChoose an option:")
        print("1. Generate Solar Birthday Subscription (Solar Input, Solar Output)")
        print("2. Generate Lunar Birthday Subscription (Solar Input, Lunar Output)")
        print("3. Generate Lunar Birthday Subscription (Lunar Input, Lunar Output)")
        print("4. Generate Solar Birthday Subscription (Lunar Input, Solar Output)")
        option = input("Enter your choice (1/2/3/4): ").strip()

        name = input("Enter the name: ").strip()

        if option == "1":
            # Solar birthday subscription
            year = int(input("Enter the solar year of birth: "))
            month = int(input("Enter the solar month of birth: "))
            day = int(input("Enter the solar day of birth: "))
            solar_date = datetime(year, month, day)
            add_birthday_event(cal, name, solar_date, "Solar")

        elif option == "2":
            # Solar input, lunar output
            year = int(input("Enter the solar year of birth: "))
            month = int(input("Enter the solar month of birth: "))
            day = int(input("Enter the solar day of birth: "))
            solar_date = datetime(year, month, day)
            lunar_date = Converter.Solar2Lunar(Solar(year, month, day))
            add_birthday_event_lunar(cal, name, lunar_date, "Lunar")

        elif option == "3":
            # Lunar input, lunar output
            year = int(input("Enter the lunar year of birth: "))
            month = int(input("Enter the lunar month of birth: "))
            day = int(input("Enter the lunar day of birth: "))
            is_leap_month = input("Is it a leap month? (yes/no): ").strip().lower() == "yes"
            lunar_date = Lunar(year, month, day, is_leap_month)
            add_birthday_event_lunar(cal, name, lunar_date, "Lunar", is_leap_month)

        elif option == "4":
            # Lunar input, solar output
            year = int(input("Enter the lunar year of birth: "))
            month = int(input("Enter the lunar month of birth: "))
            day = int(input("Enter the lunar day of birth: "))
            is_leap_month = input("Is it a leap month? (yes/no): ").strip().lower() == "yes"
            lunar_date = Lunar(year, month, day, is_leap_month)
            print(lunar_date)
            solar_date = Converter.Lunar2Solar(lunar_date)

            add_birthday_event(cal, name, solar_date, "Solar")

        else:
            print("Invalid choice. Please try again.")

        # Ask if the user wants to add another birthday
        repeat = input("Do you want to add another birthday? (yes/no): ").strip().lower()
        if repeat != "yes":
            break

    # Save the calendar to a file
    with open("birthdays.ics", "w", encoding="utf-8") as file:
        file.writelines(cal)

    print("Calendar subscription file 'birthdays.ics' has been generated!")


if __name__ == "__main__":
    main()

